import folium

def extract_coordinates(lst):
    extracted_values_list = []

    for sublist in lst:
        sub=[]
        for string in sublist:
            parts = string.split('-')
            location_name = parts[2].split(',')[0].strip()
            
            start_index = string.find('{') + 1
            end_index = string.find('}')
            
            if start_index != -1 and end_index != -1:
                data_string = string[start_index:end_index]
                data_dict = eval('{' + data_string + '}')
                data_dict['LOCATION_NAME'] = location_name
                sub.append(data_dict)
        extracted_values_list.append(sub)

    return extracted_values_list

def create_maps(extracted_values_list):
    for index, sublist in enumerate(extracted_values_list):
            map_center = [float(sublist[0]['LATITUDE']), float(sublist[0]['LONGITUDE'])]
            mymap = folium.Map(location=map_center, zoom_start=13)

            # Adding markers
            for coord in sublist:
                lat = float(coord['LATITUDE'])
                lon = float(coord['LONGITUDE'])
                location_name = coord.get('LOCATION_NAME', 'Unknown')
                popup_text = f"{location_name}"
                folium.Marker(location=[lat, lon], popup=popup_text).add_to(mymap)
            
            # Adding polyline
            points = [(float(coord['LATITUDE']), float(coord['LONGITUDE'])) for coord in sublist]
            folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(mymap)

            path = 'D:/BE/Project/Final/Travel-Planner-master/src/static/'
            mymap.save(f'{path}map{index+1}.html')


def remove_last_element(lst):
    modified_lst = []

    for sublst in lst:
        modified_sublst = []
        for item in sublst:
            parts = item.split(" - ")
            parts.pop()  # Remove the last element
            modified_sublst.append(" - ".join(parts))
        modified_lst.append(modified_sublst)
    
    return modified_lst


def main(lst):
    extracted_values_list = extract_coordinates(lst)
    create_maps(extracted_values_list)
    modified_lst = remove_last_element(lst)
    return modified_lst


