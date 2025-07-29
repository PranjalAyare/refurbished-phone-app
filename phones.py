import streamlit as st
from utils import calculate_selling_price, map_condition, MIN_PROFIT_THRESHOLD
import pandas as pd

INVENTORY_FILE = "inventory.csv"

def load_inventory():
    """Loads inventory from CSV, with robust error handling and validation."""
    try:
        df = pd.read_csv(INVENTORY_FILE)
        # Validate and clean data
        df['cost'] = pd.to_numeric(df['cost'], errors='coerce')
        df['stock'] = pd.to_numeric(df['stock'], errors='coerce')

        df.dropna(subset=['cost', 'stock'], inplace=True)


        df['cost'] = df['cost'].astype(float)
        df['stock'] = df['stock'].astype(int)
        df = df[df['cost'] >= 0]
        df = df[df['stock'] >= 0]

        return df
    except FileNotFoundError:
        st.error(f"Error: {INVENTORY_FILE} not found. Please ensure it's in the same directory.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading inventory: {e}")
        return pd.DataFrame()

def save_inventory(df):
    """Saves the current inventory DataFrame back to the CSV file."""
    try:
        df.to_csv(INVENTORY_FILE, index=False)
    except Exception as e:
        st.error(f"Error saving inventory: {e}")

def display_inventory(platform):
    st.title("📦 Inventory & Listing Suggestions")

    
    inventory_df = load_inventory()

    if inventory_df.empty:
        return

    
    processed_phones_list = []
    for index, phone in inventory_df.iterrows():
        name = phone["name"]
        condition = phone["condition"]
        cost = phone["cost"]
        stock = phone["stock"]

        platform_condition = map_condition(condition, platform)
        sell_price, fee = calculate_selling_price(cost, platform)
        profit = sell_price - cost - fee
        
        listable_stock = stock > 0
        listable_profit = profit >= MIN_PROFIT_THRESHOLD

        listable_status = "✅ Listable" if listable_stock and listable_profit else "❌ Not Listable"
        unlistable_reason = ""
        if not listable_stock:
            unlistable_reason += "Out of stock. "
        if not listable_profit:
            unlistable_reason += f"Profit (${round(profit,2)}) below threshold (${MIN_PROFIT_THRESHOLD})."

        
        processed_phones_list.append({
            "Original_Index": index,
            "Name": name,
            "Condition (Internal)": condition,
            f"Condition ({platform})": platform_condition,
            "Cost Price": cost,
            "Stock Available": stock,
            "Estimated Sell Price": sell_price,
            "Profit After Fees": profit,
            "Listing Status": listable_status,
            "Unlistable Reason": unlistable_reason.strip()
        })

    df_display = pd.DataFrame(processed_phones_list)


    st.subheader("Filters")
    col_filters = st.columns(3)
    
    with col_filters[0]:
        show_listable_only = st.checkbox("Show Only Listable Phones", value=True)
    with col_filters[1]:
        show_out_of_stock = st.checkbox("Show Out of Stock", value=False)
    with col_filters[2]:
        show_unprofitable = st.checkbox("Show Unprofitable", value=False)

    
    filtered_df = df_display.copy()
    
    if show_listable_only:
        filtered_df = filtered_df[filtered_df["Listing Status"] == "✅ Listable"]
    
    if not show_out_of_stock:
        filtered_df = filtered_df[filtered_df["Stock Available"] > 0]
    
    if not show_unprofitable:
        filtered_df = filtered_df[filtered_df['Profit After Fees'] >= MIN_PROFIT_THRESHOLD]

    st.markdown("---")
    st.subheader(f"Phones for {platform}")
    
    
    filtered_df_for_display = filtered_df.copy()
    filtered_df_for_display["Cost Price"] = filtered_df_for_display["Cost Price"].apply(lambda x: f"${x:.2f}")
    filtered_df_for_display["Estimated Sell Price"] = filtered_df_for_display["Estimated Sell Price"].apply(lambda x: f"${x:.2f}")
    filtered_df_for_display["Profit After Fees"] = filtered_df_for_display["Profit After Fees"].apply(lambda x: f"${x:.2f}")


    st.dataframe(
        filtered_df_for_display[['Name', 'Condition (Internal)', f'Condition ({platform})', 'Cost Price',
                    'Stock Available', 'Estimated Sell Price', 'Profit After Fees',
                    'Listing Status', 'Unlistable Reason']],
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")
    st.subheader("Detailed View & Sell Action (Expand for more info)")
    
    
    for _, row_display in filtered_df.iterrows():
        original_idx = row_display["Original_Index"]
        

        current_phone_data = inventory_df.loc[original_idx]

        with st.expander(f"📱 {current_phone_data['name']} - {row_display['Listing Status']}"):
            st.markdown(f"**Internal Condition:** {current_phone_data['condition']}")
            st.markdown(f"**Platform Condition ({platform}):** {row_display[f'Condition ({platform})']}")
            st.markdown(f"**Cost Price:** ${current_phone_data['cost']:.2f}")
            st.markdown(f"**Current Stock:** {current_phone_data['stock']}")
            st.markdown(f"**Estimated Sell Price ({platform}):** ${row_display['Estimated Sell Price']}")
            st.markdown(f"**Profit After Fees:** ${row_display['Profit After Fees']}")
            
            if row_display['Listing Status'] == "❌ Not Listable":
                st.warning(f"**Reason for Not Listing:** {row_display['Unlistable Reason']}")

            # --- Sell Button ---
            if current_phone_data['stock'] > 0:
                if st.button(f"Sell One {current_phone_data['name']} (B2B/Direct)", key=f"sell_{original_idx}"):
                    # Decrement stock in the main DataFrame
                    inventory_df.loc[original_idx, 'stock'] -= 1
                    save_inventory(inventory_df) # Save the updated inventory
                    st.success(f"One {current_phone_data['name']} sold! Stock is now {inventory_df.loc[original_idx, 'stock']}.")
                    st.rerun() # Rerun the app to refresh display
            else:
                st.info("No stock available to sell directly.")