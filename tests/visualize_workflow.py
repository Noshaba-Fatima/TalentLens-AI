from pathlib import Path
from app.graph.workflow import talentlens_graph

# Generate Mermaid diagram as PNG
png_data = talentlens_graph.get_graph().draw_mermaid_png()

# Save PNG in project root
output_path = Path("talentlens_workflow.png")
output_path.write_bytes(png_data)

print(f"\nGraph saved successfully: {output_path.resolve()}")