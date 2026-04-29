with open("plane_agent/api_client.py") as f:
    lines = f.readlines()

# Find the last line of the class (where to append)
last_line = len(lines)
for i in range(len(lines) - 1, -1, -1):
    if lines[i].strip() and not lines[i].startswith(" "):
        # Found something outside the class?
        pass

# Actually, I'll just append before the last method or at the end of file if it's all class.
# The class ends at 1035.

new_methods = """
    @require_auth
    def list_labels(self, project_id: str, **kwargs) -> Response:
        \"\"\"List all labels in a project.\"\"\"
        response = self._get(f"/projects/{project_id}/labels/", params=kwargs)
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def create_label(self, project_id: str, data: dict[str, Any]) -> Response:
        \"\"\"Create a new label.\"\"\"
        response = self._post(f"/projects/{project_id}/labels/", data=data)
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def retrieve_project_page(self, project_id: str, page_id: str) -> Response:
        \"\"\"Retrieve a project page by ID.\"\"\"
        response = self._get(f"/projects/{project_id}/pages/{page_id}/")
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def create_project_page(self, project_id: str, data: dict[str, Any]) -> Response:
        \"\"\"Create a new project page.\"\"\"
        response = self._post(f"/projects/{project_id}/pages/", data=data)
        response.raise_for_status()
        return Response(response=response, data=response.json())
"""

with open("plane_agent/api_client.py", "a") as f:
    f.write(new_methods)
