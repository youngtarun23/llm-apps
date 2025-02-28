import streamlit as st
import pandas as pd

def pack_items(L_c, W_c, H_c, W_max, items):
    """
    Pack items into containers using a first-fit decreasing heuristic.
    
    Args:
        L_c, W_c, H_c (float): Container dimensions.
        W_max (float): Container weight capacity.
        items (list of dict): Items with 'id', 'length', 'width', 'height', 'weight'.
    
    Returns:
        tuple: (containers, unfit_items)
            - containers (list of dict): Packing plan, or None if unfit items exist.
            - unfit_items (list of dict): Items that cannot fit individually.
    """
    volume_capacity = L_c * W_c * H_c
    for item in items:
        item['volume'] = item['length'] * item['width'] * item['height']
    
    unfit_items = [item for item in items if item['length'] > L_c or item['width'] > W_c or item['height'] > H_c]
    if unfit_items:
        return None, unfit_items
    
    sorted_items = sorted(items, key=lambda x: x['volume'], reverse=True)
    containers = []
    for item in sorted_items:
        added = False
        for container in containers:
            if (container['current_volume'] + item['volume'] <= volume_capacity and
                container['current_weight'] + item['weight'] <= W_max):
                container['items'].append(item['id'])
                container['current_volume'] += item['volume']
                container['current_weight'] += item['weight']
                added = True
                break
        if not added:
            new_container = {
                'id': len(containers) + 1,
                'items': [item['id']],
                'current_volume': item['volume'],
                'current_weight': item['weight'],
                'volume_capacity': volume_capacity,
                'weight_capacity': W_max
            }
            containers.append(new_container)
    return containers, []

# Streamlit app
st.title("Container Planning App")
st.write("Enter the container properties and item details to plan the packing. "
         "The app will assign items to the minimum number of containers, "
         "considering volume and weight constraints.")

# Container properties
st.write("## Container Properties")
container_length = st.number_input("Container Length", min_value=0.0, step=0.1, value=10.0,
                                  help="Enter the length of the container (positive number).")
container_width = st.number_input("Container Width", min_value=0.0, step=0.1, value=10.0,
                                 help="Enter the width of the container (positive number).")
container_height = st.number_input("Container Height", min_value=0.0, step=0.1, value=10.0,
                                  help="Enter the height of the container (positive number).")
container_weight_capacity = st.number_input("Container Weight Capacity", min_value=0.0, step=0.1, value=100.0,
                                           help="Enter the maximum weight the container can hold (positive number).")

# Item details
st.write("## Items")
st.write("Add, edit, or remove items below. Each item must have a unique ID and positive dimensions and weight.")
default_items = pd.DataFrame({
    'id': [1, 2, 3],
    'length': [2.0, 5.0, 3.0],
    'width': [3.0, 5.0, 3.0],
    'height': [4.0, 5.0, 3.0],
    'weight': [10.0, 20.0, 15.0]
})
items_df = st.data_editor(
    default_items,
    num_rows="dynamic",
    column_config={
        "id": st.column_config.NumberColumn("ID", min_value=1, step=1,
                                            help="Unique integer identifier for the item."),
        "length": st.column_config.NumberColumn("Length", min_value=0.0, step=0.1,
                                                help="Length of the item (positive number)."),
        "width": st.column_config.NumberColumn("Width", min_value=0.0, step=0.1,
                                               help="Width of the item (positive number)."),
        "height": st.column_config.NumberColumn("Height", min_value=0.0, step=0.1,
                                                help="Height of the item (positive number)."),
        "weight": st.column_config.NumberColumn("Weight", min_value=0.0, step=0.1,
                                                help="Weight of the item (positive number)."),
    },
    hide_index=True,
)

# Run packing algorithm
if st.button("Run Packing Algorithm"):
    if container_length <= 0 or container_width <= 0 or container_height <= 0 or container_weight_capacity <= 0:
        st.error("Container dimensions and weight capacity must be positive.")
    elif items_df.empty:
        st.error("Please add at least one item.")
    else:
        items = items_df.to_dict('records')
        containers, unfit_items = pack_items(container_length, container_width, container_height,
                                            container_weight_capacity, items)
        if unfit_items:
            unfit_ids = [item['id'] for item in unfit_items]
            st.error(f"The following items cannot fit in the container individually due to size constraints: {unfit_ids}")
            st.write("Please adjust the dimensions of these items or the container properties and try again.")
        else:
            st.success("Packing completed successfully!")
            st.write(f"**Total number of containers used:** {len(containers)}")
            st.write("### Packing Plan")
            for container in containers:
                st.subheader(f"Container {container['id']}")
                st.write(f"**Items assigned (IDs):** {container['items']}")
                st.write(f"**Volume used:** {container['current_volume']:.2f} / {container['volume_capacity']:.2f}")
                st.write(f"**Weight used:** {container['current_weight']:.2f} / {container['weight_capacity']:.2f}")