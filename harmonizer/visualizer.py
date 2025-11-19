#!/usr/bin/env python3
"""
Harmonizer Visualizer - Generates interactive HTML dashboards for LJPW analysis.
"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime


class HarmonizerVisualizer:
    """
    Generates a self-contained HTML report with interactive visualizations.
    Uses Chart.js for charts and D3.js for force-directed graphs.
    """

    def __init__(self, output_path: str = "harmonizer_report.html"):
        self.output_path = output_path

    def generate_report(
        self,
        file_analyses: Dict[str, Any],
        dependency_graph: Dict[str, Any],
        project_name: str = "Project Analysis",
    ):
        """
        Generates the HTML report.

        Args:
            file_analyses: Dict mapping file paths to analysis data (including LJPW coords)
            dependency_graph: Dict with nodes and links for D3 graph
            project_name: Name of the project
        """

        # Prepare data for JavaScript
        js_data = {
            "files": self._prepare_file_data(file_analyses),
            "graph": dependency_graph,
            "timestamp": datetime.now().isoformat(),
            "project": project_name,
        }

        html_content = self._get_html_template(js_data)

        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"Report generated: {os.path.abspath(self.output_path)}")

    def _prepare_file_data(self, file_analyses: Dict[str, Any]) -> List[Dict]:
        """Convert python objects to JSON-serializable list"""
        data = []
        for path, analysis in file_analyses.items():
            # Handle both object and dict access (depending on how it's passed)
            if hasattr(analysis, "coordinates"):
                coords = analysis.coordinates
                func_count = analysis.function_count
                density = getattr(analysis, "semantic_density", 0.0)
                disharmony = analysis.avg_disharmony
            else:
                coords = analysis.get("coordinates", (0, 0, 0, 0))
                func_count = analysis.get("function_count", 0)
                density = analysis.get("semantic_density", 0.0)
                disharmony = analysis.get("avg_disharmony", 0.0)

            data.append(
                {
                    "path": path,
                    "name": os.path.basename(path),
                    "l": coords[0],
                    "j": coords[1],
                    "p": coords[2],
                    "w": coords[3],
                    "functions": func_count,
                    "density": density,
                    "disharmony": disharmony,
                }
            )
        return data

    def _get_html_template(self, data: Dict) -> str:
        """Returns the full HTML content with embedded data and scripts"""
        json_data = json.dumps(data)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LJPW Harmonizer Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        :root {{
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent: #38bdf8;
            --love: #f472b6;
            --justice: #fbbf24;
            --power: #ef4444;
            --wisdom: #3b82f6;
        }}
        
        body {{
            font-family: 'Inter', system-ui, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-primary);
            margin: 0;
            padding: 20px;
        }}
        
        .container {{
            max_width: 1400px;
            margin: 0 auto;
        }}
        
        header {{
            margin-bottom: 30px;
            border-bottom: 1px solid #334155;
            padding-bottom: 20px;
        }}
        
        h1 {{ margin: 0; font-size: 2rem; }}
        .subtitle {{ color: var(--text-secondary); margin-top: 5px; }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .card {{
            background-color: var(--card-bg);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}
        
        .card h2 {{ margin-top: 0; font-size: 1.2rem; color: var(--accent); }}
        
        #galaxy-graph {{
            width: 100%;
            height: 600px;
            background-color: #020617;
            border-radius: 8px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }}
        
        th, td {{
            text-align: left;
            padding: 12px;
            border-bottom: 1px solid #334155;
        }}
        
        th {{ color: var(--text-secondary); font-weight: 600; }}
        
        .badge {{
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: bold;
        }}
        
        .badge-love {{ background: rgba(244, 114, 182, 0.2); color: var(--love); }}
        .badge-justice {{ background: rgba(251, 191, 36, 0.2); color: var(--justice); }}
        .badge-power {{ background: rgba(239, 68, 68, 0.2); color: var(--power); }}
        .badge-wisdom {{ background: rgba(59, 130, 246, 0.2); color: var(--wisdom); }}
        
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>LJPW Code Harmony Report</h1>
            <div class="subtitle">Generated on {datetime.now().strftime("%Y-%m-%d %H:%M")}</div>
        </header>
        
        <div class="grid">
            <div class="card">
                <h2>System Balance (Average)</h2>
                <canvas id="radarChart"></canvas>
            </div>
            <div class="card">
                <h2>Semantic Density vs Complexity</h2>
                <canvas id="scatterChart"></canvas>
            </div>
        </div>
        
        <div class="card" style="margin-bottom: 30px;">
            <h2>Dependency Galaxy (Gravitational Pull)</h2>
            <div id="galaxy-graph"></div>
            <p style="color: var(--text-secondary); font-size: 0.9rem; margin-top: 10px;">
                Nodes are sized by Mass (Complexity). Links show imports. 
                Colors represent dominant LJPW dimension.
            </p>
        </div>
        
        <div class="card">
            <h2>File Analysis</h2>
            <div style="overflow-x: auto;">
                <table id="fileTable">
                    <thead>
                        <tr>
                            <th>File</th>
                            <th>Dominant</th>
                            <th>L</th>
                            <th>J</th>
                            <th>P</th>
                            <th>W</th>
                            <th>Density</th>
                            <th>Disharmony</th>
                        </tr>
                    </thead>
                    <tbody></tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        const data = {json_data};
        
        // --- 1. Radar Chart ---
        const avgL = data.files.reduce((sum, f) => sum + f.l, 0) / data.files.length;
        const avgJ = data.files.reduce((sum, f) => sum + f.j, 0) / data.files.length;
        const avgP = data.files.reduce((sum, f) => sum + f.p, 0) / data.files.length;
        const avgW = data.files.reduce((sum, f) => sum + f.w, 0) / data.files.length;
        
        new Chart(document.getElementById('radarChart'), {{
            type: 'radar',
            data: {{
                labels: ['Love (Unity)', 'Justice (Order)', 'Power (Agency)', 'Wisdom (Truth)'],
                datasets: [{{
                    label: 'System Average',
                    data: [avgL, avgJ, avgP, avgW],
                    backgroundColor: 'rgba(56, 189, 248, 0.2)',
                    borderColor: '#38bdf8',
                    pointBackgroundColor: '#38bdf8'
                }}, {{
                    label: 'Natural Equilibrium',
                    data: [0.618, 0.414, 0.718, 0.693],
                    backgroundColor: 'rgba(148, 163, 184, 0.1)',
                    borderColor: '#94a3b8',
                    borderDash: [5, 5],
                    pointRadius: 0
                }}]
            }},
            options: {{
                scales: {{
                    r: {{
                        beginAtZero: true,
                        max: 1.5,
                        grid: {{ color: '#334155' }},
                        pointLabels: {{ color: '#cbd5e1' }},
                        ticks: {{ display: false }}
                    }}
                }},
                plugins: {{ legend: {{ labels: {{ color: '#cbd5e1' }} }} }}
            }}
        }});
        
        // --- 2. Scatter Chart (Density vs Complexity) ---
        new Chart(document.getElementById('scatterChart'), {{
            type: 'scatter',
            data: {{
                datasets: [{{
                    label: 'Files',
                    data: data.files.map(f => ({{ x: f.functions, y: f.density, name: f.name }})),
                    backgroundColor: data.files.map(f => {{
                        const max = Math.max(f.l, f.j, f.p, f.w);
                        if (max === f.l) return '#f472b6';
                        if (max === f.j) return '#fbbf24';
                        if (max === f.p) return '#ef4444';
                        return '#3b82f6';
                    }})
                }}]
            }},
            options: {{
                scales: {{
                    x: {{ 
                        title: {{ display: true, text: 'Complexity (Function Count)', color: '#94a3b8' }},
                        grid: {{ color: '#334155' }},
                        ticks: {{ color: '#94a3b8' }}
                    }},
                    y: {{ 
                        title: {{ display: true, text: 'Semantic Density (Power/LOC)', color: '#94a3b8' }},
                        grid: {{ color: '#334155' }},
                        ticks: {{ color: '#94a3b8' }}
                    }}
                }},
                plugins: {{
                    tooltip: {{
                        callbacks: {{
                            label: (ctx) => ctx.raw.name
                        }}
                    }},
                    legend: {{ display: false }}
                }}
            }}
        }});
        
        // --- 3. D3 Force Graph ---
        const width = document.getElementById('galaxy-graph').clientWidth;
        const height = 600;
        
        const svg = d3.select("#galaxy-graph").append("svg")
            .attr("width", width)
            .attr("height", height);
            
        const simulation = d3.forceSimulation(data.graph.nodes)
            .force("link", d3.forceLink(data.graph.links).id(d => d.id).distance(100))
            .force("charge", d3.forceManyBody().strength(-300))
            .force("center", d3.forceCenter(width / 2, height / 2));
            
        const link = svg.append("g")
            .selectAll("line")
            .data(data.graph.links)
            .enter().append("line")
            .attr("stroke", "#475569")
            .attr("stroke-width", 1);
            
        const node = svg.append("g")
            .selectAll("circle")
            .data(data.graph.nodes)
            .enter().append("circle")
            .attr("r", d => 5 + Math.sqrt(d.mass) * 2)
            .attr("fill", d => {{
                // Color by dominant dimension
                // We need to find the file analysis for this node
                const file = data.files.find(f => f.path.endsWith(d.id));
                if (!file) return "#94a3b8";
                const max = Math.max(file.l, file.j, file.p, file.w);
                if (max === file.l) return '#f472b6';
                if (max === file.j) return '#fbbf24';
                if (max === file.p) return '#ef4444';
                return '#3b82f6';
            }})
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));
                
        node.append("title").text(d => d.id);
        
        simulation.on("tick", () => {{
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);
                
            node
                .attr("cx", d => d.x)
                .attr("cy", d => d.y);
        }});
        
        function dragstarted(event, d) {{
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }}
        
        function dragged(event, d) {{
            d.fx = event.x;
            d.fy = event.y;
        }}
        
        function dragended(event, d) {{
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }}
        
        // --- 4. Populate Table ---
        const tbody = document.querySelector('#fileTable tbody');
        data.files.forEach(f => {{
            const tr = document.createElement('tr');
            
            const max = Math.max(f.l, f.j, f.p, f.w);
            let domClass = '';
            let domName = '';
            if (max === f.l) {{ domClass = 'badge-love'; domName = 'Love'; }}
            else if (max === f.j) {{ domClass = 'badge-justice'; domName = 'Justice'; }}
            else if (max === f.p) {{ domClass = 'badge-power'; domName = 'Power'; }}
            else {{ domClass = 'badge-wisdom'; domName = 'Wisdom'; }}
            
            tr.innerHTML = `
                <td>${{f.name}}</td>
                <td><span class="badge ${{domClass}}">${{domName}}</span></td>
                <td>${{f.l.toFixed(2)}}</td>
                <td>${{f.j.toFixed(2)}}</td>
                <td>${{f.p.toFixed(2)}}</td>
                <td>${{f.w.toFixed(2)}}</td>
                <td>${{f.density.toFixed(2)}}</td>
                <td>${{f.disharmony.toFixed(2)}}</td>
            `;
            tbody.appendChild(tr);
        }});
    </script>
</body>
</html>"""
