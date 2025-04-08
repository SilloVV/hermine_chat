import json

name_searched : str = "legi"
def extract_post_paths(json_file_path):
    """
    Extract POST paths and their descriptions from a Swagger/OpenAPI JSON specification.
    
    Args:
        json_file_path (str): Path to the JSON specification file
    
    Returns:
        list: A list of dictionaries containing path and description
    """
    # Read the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as file:
        api_spec = json.load(file)
    
    # List to store extracted paths
    post_paths = []
    
    # Iterate through paths
    for path, path_details in api_spec.get('paths', {}).items():
        # Check if the path has a POST method
        if 'post' in path_details:
            # Extract description from the POST method
            description = path_details['post'].get('description', 'No description provided')
            
            # Create a dictionary for the path and its description
            post_paths.append({
                'path': path,
                'description': description
            })
    
    return post_paths

# Example usage
def main():
    json_file_path = 'juri_api_spec.json'
    
    try:
        paths = extract_post_paths(json_file_path)
        
        # Print the extracted paths and descriptions
        print("POST Paths in the API:")
        for path_info in paths:
            print(f"\nPath: {path_info['path']}")
            print(f"Description: {path_info['description']}")
    
    except FileNotFoundError:
        print(f"Error: File {json_file_path} not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON file.")

if __name__ == '__main__':
    main()