#!/usr/bin/env python3
import time
import os
from collections import deque
from datetime import datetime
from ping3 import ping
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns

class NetworkMonitor:
    def __init__(self, host="8.8.8.8", interval=2, max_history=450):
        self.host = host
        self.interval = interval
        self.max_history = max_history  # 15 minutes at 2sec intervals
        self.history = deque(maxlen=max_history)
        self.console = Console()
        
    def check_connection(self):
        try:
            response_time = ping(self.host, timeout=3)
            if response_time is not None:
                return True, int(response_time * 1000)  # Convert to ms
            return False, 0
        except:
            return False, 0
    
    def get_stats(self):
        if not self.history:
            return 0, 0, 0
        
        connected = sum(1 for _, status, _ in self.history if status)
        total = len(self.history)
        uptime = (connected / total) * 100 if total > 0 else 0
        
        response_times = [rt for _, status, rt in self.history if status and rt > 0]
        avg_response = sum(response_times) / len(response_times) if response_times else 0
        
        return uptime, avg_response, total
    
    def get_time_averages(self):
        if not self.history:
            return {}
        
        now = datetime.now()
        averages = {}
        
        # Time periods in seconds
        periods = {'1m': 60, '5m': 300, '15m': 900, '30m': 1800}
        
        for period_name, seconds in periods.items():
            period_data = []
            for timestamp, status, rt in self.history:
                if (now - timestamp).total_seconds() <= seconds and status and rt > 0:
                    period_data.append(rt)
            
            if period_data:
                averages[period_name] = sum(period_data) / len(period_data)
            else:
                averages[period_name] = 0
        
        return averages
    
    def create_ascii_graph(self, width=90):  # 3 minutes at 2sec intervals
        if len(self.history) < 2:
            return Text("No data yet...", style="dim")
        
        # Get recent data
        recent_data = list(self.history)[-width:]
        response_times = []
        timestamps = []
        
        for timestamp, status, rt in recent_data:
            response_times.append(rt if status and rt > 0 else None)
            timestamps.append(timestamp)
        
        valid_times = [rt for rt in response_times if rt is not None]
        if not valid_times:
            return Text("All connections failed", style="red")
        
        # Calculate scale
        max_rt = max(valid_times)
        min_rt = min(valid_times)
        if max_rt - min_rt < 50:
            max_rt = min_rt + 100
        
        height = 8
        graph_text = Text()
        
        # Create graph lines
        for i in range(height):
            y_value = max_rt - (i * (max_rt - min_rt) / (height - 1))
            line_text = Text()
            line_text.append(f"{int(y_value):3d}ms ┤", style="dim")
            
            for j, rt in enumerate(response_times):
                if rt is None:
                    if i == height // 2:
                        line_text.append("×", style="red")
                    else:
                        line_text.append(" ")
                else:
                    normalized_pos = (rt - min_rt) / (max_rt - min_rt) if max_rt > min_rt else 0.5
                    graph_pos = int(normalized_pos * (height - 1))
                    
                    if i == height - 1 - graph_pos:
                        if rt < 30:
                            line_text.append("●", style="dark_green")
                        elif rt < 50:
                            line_text.append("●", style="yellow")
                        elif rt < 100:
                            line_text.append("●", style="white")
                        elif rt < 300:
                            line_text.append("●", style="red")
                        else:
                            line_text.append("●", style="magenta")
                    else:
                        # Connect with previous point
                        if j > 0 and response_times[j-1] is not None:
                            prev_rt = response_times[j-1]
                            prev_pos = int(((prev_rt - min_rt) / (max_rt - min_rt)) * (height - 1))
                            if abs((height - 1 - i) - prev_pos) <= 1:
                                line_text.append("─", style="dim")
                            else:
                                line_text.append(" ")
                        else:
                            line_text.append(" ")
            
            graph_text.append_text(line_text)
            if i < height - 1:
                graph_text.append("\n")
        
        # Add X-axis
        graph_text.append("\n")
        x_axis = Text()
        x_axis.append("     └", style="dim")
        x_axis.append("─" * len(response_times), style="dim")
        graph_text.append_text(x_axis)
        
        # Add time labels
        if timestamps:
            graph_text.append("\n")
            time_text = Text()
            time_text.append("      ", style="dim")
            
            now = timestamps[-1]
            # Show start time and end time
            start_diff = (now - timestamps[0]).total_seconds()
            if start_diff < 60:
                start_label = f"{int(start_diff)}s ago"
            else:
                start_label = f"{int(start_diff/60)}m ago"
            
            time_text.append(start_label, style="dim")
            
            # Pad to end
            padding = len(response_times) - len(start_label) - 3
            if padding > 0:
                time_text.append(" " * padding)
            time_text.append("now", style="dim")
            
            graph_text.append_text(time_text)
        
        return graph_text
    
    def create_status_line(self, count=20):
        if not self.history:
            return Text("No data", style="dim")
        
        recent = list(self.history)[-count:]
        status_text = Text()
        
        for _, status, rt in recent:
            if status:
                if rt < 30:
                    status_text.append("●", style="dark_green")
                elif rt < 50:
                    status_text.append("●", style="yellow")
                elif rt < 100:
                    status_text.append("●", style="white")
                elif rt < 300:
                    status_text.append("●", style="red")
                else:
                    status_text.append("●", style="magenta")
            else:
                status_text.append("×", style="red")
        
        return status_text
    
    def create_display(self):
        if not self.history:
            current_status = "[yellow]Checking...[/yellow]"
            current_rt = 0
        else:
            _, last_status, last_rt = self.history[-1]
            if last_status:
                if last_rt < 30:
                    current_status = f"[dark_green]✓ Excellent ({last_rt}ms)[/dark_green]"
                elif last_rt < 50:
                    current_status = f"[yellow]✓ Good ({last_rt}ms)[/yellow]"
                elif last_rt < 100:
                    current_status = f"[white]⚠ Fair ({last_rt}ms)[/white]"
                elif last_rt < 300:
                    current_status = f"[red]⚠ Slow ({last_rt}ms)[/red]"
                else:
                    current_status = f"[magenta]⚠ Very Slow ({last_rt}ms)[/magenta]"
            else:
                current_status = "[red]✗ Disconnected[/red]"
        
        uptime, avg_rt, total_checks = self.get_stats()
        
        # Header
        header = Text()
        header.append("Network Monitor", style="bold blue")
        header.append(f" - {datetime.now().strftime('%H:%M:%S')}", style="dim")
        
        # Status info
        status_info = Text()
        status_info.append("Status: ")
        status_info.append_text(Text.from_markup(current_status))
        status_info.append(f"  Uptime: {uptime:.1f}%")
        
        # Time-based averages
        time_avgs = self.get_time_averages()
        avg_info = Text()
        avg_info.append("Averages: ")
        for period, avg in time_avgs.items():
            if avg > 0:
                avg_info.append(f"{period}:{avg:.0f}ms  ")
            else:
                avg_info.append(f"{period}:--  ")
        
        # Graph with title
        graph = self.create_ascii_graph()
        graph_title = Text()
        graph_title.append("Response Time Trend (Last 3 minutes)", style="bold")
        if valid_times := [rt for _, status, rt in self.history if status and rt > 0]:
            graph_title.append(f" ({min(valid_times)}-{max(valid_times)}ms)", style="dim")
        
        # Recent status
        status_line = self.create_status_line()
        recent_text = Text()
        recent_text.append("Recent: ")
        recent_text.append_text(status_line)
        recent_text.append(f" ({total_checks} checks)")
        
        # Legend
        legend = Text()
        legend.append("Legend: ")
        legend.append("●", style="dark_green")
        legend.append(" <30ms  ")
        legend.append("●", style="yellow")
        legend.append(" 30-50ms  ")
        legend.append("●", style="white")
        legend.append(" 50-100ms  ")
        legend.append("●", style="red")
        legend.append(" 100-300ms  ")
        legend.append("●", style="magenta")
        legend.append(" >300ms  ")
        legend.append("×", style="red")
        legend.append(" Disconnected")
        
        # Combine all
        content = Text()
        content.append_text(header)
        content.append("\n\n")
        content.append_text(status_info)
        content.append("\n")
        content.append_text(avg_info)
        content.append("\n\n")
        content.append_text(graph_title)
        content.append("\n")
        content.append_text(graph)
        content.append("\n\n")
        content.append_text(legend)
        content.append("\n\n")
        content.append_text(recent_text)
        content.append("\n\nPress Ctrl+C to stop")
        
        return Panel(content, title="NetCheck", border_style="blue")
    
    def run(self):
        try:
            with Live(self.create_display(), refresh_per_second=1, screen=True) as live:
                while True:
                    timestamp = datetime.now()
                    is_connected, response_time = self.check_connection()
                    
                    self.history.append((timestamp, is_connected, response_time))
                    live.update(self.create_display())
                    
                    time.sleep(self.interval)
                    
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Monitoring stopped.[/yellow]")
            
            # Show final stats
            uptime, avg_rt, total = self.get_stats()
            self.console.print(f"\nFinal Stats:")
            self.console.print(f"Total checks: {total}")
            self.console.print(f"Uptime: {uptime:.1f}%")
            if avg_rt > 0:
                self.console.print(f"Average response: {avg_rt:.0f}ms")

if __name__ == "__main__":
    monitor = NetworkMonitor()
    monitor.run()