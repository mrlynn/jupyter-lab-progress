from IPython.display import display, HTML, Markdown
from typing import Optional, Dict, Any
import json
import re

def _format_message(message: str) -> str:
    """Format a message for HTML display, handling line breaks and basic formatting."""
    # Convert newlines to HTML line breaks
    formatted = message.replace('\n', '<br>')
    
    # Convert numbered lists (1. item, 2. item, etc.)
    formatted = re.sub(r'^(\d+\.\s)', r'<br>&nbsp;&nbsp;\1', formatted, flags=re.MULTILINE)
    
    # Convert bullet points (- item or * item)
    formatted = re.sub(r'^([-*]\s)', r'<br>&nbsp;&nbsp;•&nbsp;', formatted, flags=re.MULTILINE)
    
    # Clean up any leading <br> tags
    formatted = re.sub(r'^<br>', '', formatted)
    
    return formatted

def show_info(message: str, title: Optional[str] = None, collapsible: bool = False, 
              expanded: bool = True, hint: Optional[str] = None):
    """Display an information message with blue styling.
    
    Args:
        message: The main message to display
        title: Optional title for the message
        collapsible: Whether the message should be collapsible
        expanded: If collapsible, whether to start expanded
        hint: Optional hint text to show in a collapsible section
    """
    import uuid
    info_id = str(uuid.uuid4())
    
    title_html = f"<strong>{title}</strong><br>" if title else ""
    formatted_message = _format_message(message)
    
    # Add hint section if provided
    hint_html = ""
    if hint:
        hint_html = f"""
        <details style='margin-top: 10px; background-color: #d6e9ff; padding: 8px; 
                        border-radius: 4px;'>
            <summary style='cursor: pointer; color: #1976d2; font-weight: 500;'>
                💡 Hint (click to expand)
            </summary>
            <div style='margin-top: 8px; padding-left: 15px;'>{_format_message(hint)}</div>
        </details>
        """
    
    if collapsible:
        display(HTML(f"""
        <details {'open' if expanded else ''} style='margin: 10px 0;'>
            <summary style='cursor: pointer; background-color: #e7f3ff; 
                           border-left: 6px solid #2196F3; padding: 10px; 
                           border-radius: 5px; display: block;'>
                <span style='font-size: 16px; margin-right: 8px;'>ℹ️</span>
                {title or 'Information'} (click to toggle)
            </summary>
            <div style='background-color: #f5f9ff; padding: 15px; margin-top: 5px; 
                        border-left: 6px solid #2196F3; border-radius: 0 0 5px 5px;'>
                {formatted_message}
                {hint_html}
            </div>
        </details>
        """))
    else:
        display(HTML(f"""
        <div style='background-color: #e7f3ff; border-left: 6px solid #2196F3; 
                    padding: 10px; margin: 10px 0; border-radius: 5px;'>
            <span style='font-size: 16px; margin-right: 8px;'>ℹ️</span>
            {title_html}{formatted_message}
            {hint_html}
        </div>
        """))

def show_warning(message: str, title: Optional[str] = None):
    """Display a warning message with yellow styling."""
    title_html = f"<strong>{title}</strong><br>" if title else ""
    formatted_message = _format_message(message)
    display(HTML(f"""
    <div style='background-color: #fff3cd; border-left: 6px solid #ffecb5; 
                padding: 10px; margin: 10px 0; border-radius: 5px;'>
        <span style='font-size: 16px; margin-right: 8px;'>⚠️</span>
        {title_html}{formatted_message}
    </div>
    """))

def show_error(message: str, title: Optional[str] = None):
    """Display an error message with red styling."""
    title_html = f"<strong>{title}</strong><br>" if title else ""
    formatted_message = _format_message(message)
    display(HTML(f"""
    <div style='background-color: #ffebee; border-left: 6px solid #f44336; 
                padding: 10px; margin: 10px 0; border-radius: 5px;'>
        <span style='font-size: 16px; margin-right: 8px;'>❌</span>
        {title_html}{formatted_message}
    </div>
    """))

def show_success(message: str, title: Optional[str] = None):
    """Display a success message with green styling."""
    title_html = f"<strong>{title}</strong><br>" if title else ""
    formatted_message = _format_message(message)
    display(HTML(f"""
    <div style='background-color: #e8f5e9; border-left: 6px solid #4CAF50; 
                padding: 10px; margin: 10px 0; border-radius: 5px;'>
        <span style='font-size: 16px; margin-right: 8px;'>✅</span>
        {title_html}{formatted_message}
    </div>
    """))

def show_code(code: str, language: str = "python", title: Optional[str] = None):
    """Display code with syntax highlighting."""
    title_html = f"<h4 style='margin-bottom: 10px;'>{title}</h4>" if title else ""
    display(HTML(f"""
    {title_html}
    <pre style='background-color: #f5f5f5; padding: 15px; border-radius: 5px; 
                overflow-x: auto; border: 1px solid #ddd;'>
        <code class='language-{language}'>{code}</code>
    </pre>
    """))

def show_hint(hint: str, title: str = "Hint", icon: str = "💡", 
              context: Optional[str] = None):
    """Display a collapsible hint.
    
    Args:
        hint: The hint text to display
        title: Title for the hint
        icon: Icon to display (default: 💡)
        context: Optional context information to show above the hint
    """
    import uuid
    hint_id = str(uuid.uuid4())
    
    context_html = ""
    if context:
        context_html = f"<div style='margin-bottom: 10px; color: #666;'>{_format_message(context)}</div>"
    
    display(HTML(f"""
    <details style='background-color: #f0f7ff; padding: 10px; margin: 10px 0; 
                     border-radius: 5px; border: 1px solid #90caf9;'>
        <summary style='cursor: pointer; font-weight: bold; color: #1976d2;'>
            {icon} {title} (click to expand)
        </summary>
        <div style='margin-top: 10px; padding-left: 20px;'>
            {context_html}
            {_format_message(hint)}
        </div>
    </details>
    """))

def show_progress_bar(current: int, total: int, label: str = "", 
                     color: str = "#4CAF50"):
    """Display a progress bar."""
    percentage = (current / total) * 100 if total > 0 else 0
    display(HTML(f"""
    <div style='margin: 10px 0;'>
        {f"<div style='margin-bottom: 5px;'>{label}</div>" if label else ""}
        <div style='background-color: #e0e0e0; border-radius: 10px; height: 25px;'>
            <div style='background-color: {color}; height: 100%; border-radius: 10px; 
                        width: {percentage}%; transition: width 0.3s ease;
                        display: flex; align-items: center; padding-left: 10px;'>
                <span style='color: white; font-size: 12px; font-weight: bold;'>
                    {current}/{total} ({percentage:.0f}%)
                </span>
            </div>
        </div>
    </div>
    """))

def show_json(data: Dict[str, Any], title: Optional[str] = None, 
              collapsed: bool = False):
    """Display JSON data in a formatted, collapsible view."""
    import uuid
    json_id = str(uuid.uuid4())
    json_str = json.dumps(data, indent=2)
    
    if collapsed:
        display(HTML(f"""
        <details style='margin: 10px 0;'>
            <summary style='cursor: pointer; font-weight: bold; 
                           background-color: #f5f5f5; padding: 10px; 
                           border-radius: 5px;'>
                {title or 'JSON Data'} (click to expand)
            </summary>
            <pre style='background-color: #f8f8f8; padding: 15px; 
                        border-radius: 5px; overflow-x: auto; 
                        border: 1px solid #ddd; margin-top: 5px;'>
                <code>{json_str}</code>
            </pre>
        </details>
        """))
    else:
        title_html = f"<h4>{title}</h4>" if title else ""
        display(HTML(f"""
        {title_html}
        <pre style='background-color: #f8f8f8; padding: 15px; 
                    border-radius: 5px; overflow-x: auto; 
                    border: 1px solid #ddd; margin: 10px 0;'>
            <code>{json_str}</code>
        </pre>
        """))

def show_table(headers: list, rows: list, title: Optional[str] = None):
    """Display data in a formatted table."""
    title_html = f"<h4>{title}</h4>" if title else ""
    
    header_html = "".join(f"<th style='padding: 10px; text-align: left; background-color: #f5f5f5;'>{h}</th>" 
                         for h in headers)
    
    rows_html = ""
    for i, row in enumerate(rows):
        bg_color = "#ffffff" if i % 2 == 0 else "#f9f9f9"
        row_html = "".join(f"<td style='padding: 10px; border-bottom: 1px solid #ddd;'>{cell}</td>" 
                          for cell in row)
        rows_html += f"<tr style='background-color: {bg_color};'>{row_html}</tr>"
    
    display(HTML(f"""
    {title_html}
    <table style='border-collapse: collapse; width: 100%; margin: 10px 0; 
                  border: 1px solid #ddd;'>
        <thead>
            <tr>{header_html}</tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
    """))

def show_checklist(items: Dict[str, bool], title: str = "Checklist"):
    """Display a checklist with checked/unchecked items."""
    items_html = ""
    for item, checked in items.items():
        icon = "✅" if checked else "⬜"
        style = "color: #4CAF50;" if checked else "color: #666;"
        items_html += f"<li style='{style} list-style: none; margin: 5px 0;'>{icon} {item}</li>"
    
    display(HTML(f"""
    <div style='background-color: #f9f9f9; padding: 15px; 
                border-radius: 5px; margin: 10px 0;'>
        <h4 style='margin-top: 0;'>{title}</h4>
        <ul style='padding-left: 0; margin-bottom: 0;'>
            {items_html}
        </ul>
    </div>
    """))

def show_tabs(tabs: Dict[str, str], default_tab: Optional[str] = None):
    """Display content in tabs."""
    import uuid
    tab_id = str(uuid.uuid4())
    
    if not default_tab:
        default_tab = list(tabs.keys())[0]
    
    tab_buttons = ""
    tab_contents = ""
    
    for i, (tab_name, content) in enumerate(tabs.items()):
        active = tab_name == default_tab
        button_style = """
            padding: 10px 20px; 
            background-color: {bg}; 
            border: 1px solid #ddd; 
            border-bottom: none; 
            cursor: pointer;
            border-radius: 5px 5px 0 0;
            margin-right: 5px;
        """.format(bg="#fff" if active else "#f5f5f5")
        
        content_style = f"""
            padding: 20px; 
            background-color: #fff; 
            border: 1px solid #ddd;
            border-radius: 0 5px 5px 5px;
            display: {'block' if active else 'none'};
        """
        
        tab_buttons += f"""
            <button id="tab-btn-{tab_id}-{i}" 
                    onclick="showTab('{tab_id}', {i})"
                    style="{button_style}">
                {tab_name}
            </button>
        """
        
        tab_contents += f"""
            <div id="tab-content-{tab_id}-{i}" style="{content_style}">
                {content}
            </div>
        """
    
    display(HTML(f"""
    <div style='margin: 10px 0;'>
        <div style='margin-bottom: -1px;'>
            {tab_buttons}
        </div>
        <div>
            {tab_contents}
        </div>
    </div>
    <script>
    function showTab(tabId, index) {{
        // Hide all tabs
        var contents = document.querySelectorAll('[id^="tab-content-' + tabId + '"]');
        var buttons = document.querySelectorAll('[id^="tab-btn-' + tabId + '"]');
        
        for (var i = 0; i < contents.length; i++) {{
            contents[i].style.display = 'none';
            buttons[i].style.backgroundColor = '#f5f5f5';
        }}
        
        // Show selected tab
        document.getElementById('tab-content-' + tabId + '-' + index).style.display = 'block';
        document.getElementById('tab-btn-' + tabId + '-' + index).style.backgroundColor = '#fff';
    }}
    </script>
    """))

def clear():
    """Clear the output area."""
    from IPython.display import clear_output
    clear_output(wait=True)

def show_contextual_tips(tips: Dict[str, str], title: str = "Tips for this step",
                        style: str = "info"):
    """Display multiple contextual tips in an organized format.
    
    Args:
        tips: Dictionary of tip categories and their content
        title: Overall title for the tips section
        style: Visual style ('info', 'warning', 'success')
    """
    styles = {
        'info': {'bg': '#e7f3ff', 'border': '#2196F3', 'icon': '💡'},
        'warning': {'bg': '#fff3cd', 'border': '#ffecb5', 'icon': '⚠️'},
        'success': {'bg': '#e8f5e9', 'border': '#4CAF50', 'icon': '✅'}
    }
    
    style_config = styles.get(style, styles['info'])
    
    tips_html = ""
    for category, tip in tips.items():
        tips_html += f"""
        <div style='margin: 8px 0; padding: 8px 12px; background-color: rgba(255,255,255,0.5); 
                    border-left: 3px solid {style_config['border']}; border-radius: 3px;'>
            <strong style='color: #333;'>{category}:</strong>
            <div style='margin-top: 4px; color: #555;'>{_format_message(tip)}</div>
        </div>
        """
    
    display(HTML(f"""
    <div style='background-color: {style_config['bg']}; padding: 15px; 
                margin: 10px 0; border-radius: 5px; border: 1px solid {style_config['border']};'>
        <h4 style='margin: 0 0 10px 0; color: #333;'>
            {style_config['icon']} {title}
        </h4>
        {tips_html}
    </div>
    """))

def show_step_guidance(step_name: str, instructions: str, tips: Optional[Dict[str, str]] = None,
                      hints: Optional[list] = None, common_mistakes: Optional[list] = None):
    """Display comprehensive guidance for a lab step.
    
    Args:
        step_name: Name of the current step
        instructions: Main instructions for the step
        tips: Optional dictionary of tips by category
        hints: Optional list of progressive hints
        common_mistakes: Optional list of common mistakes to avoid
    """
    display(HTML(f"""
    <div style='background-color: #f8f9fa; padding: 20px; margin: 15px 0; 
                border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
        <h3 style='margin: 0 0 15px 0; color: #1976d2;'>📋 {step_name}</h3>
        <div style='background-color: white; padding: 15px; border-radius: 5px; 
                    margin-bottom: 15px;'>
            <h4 style='margin: 0 0 10px 0; color: #333;'>Instructions:</h4>
            <div style='color: #555;'>{_format_message(instructions)}</div>
        </div>
    </div>
    """))
    
    # Show tips if provided
    if tips:
        show_contextual_tips(tips, "Tips for this step")
    
    # Show progressive hints if provided
    if hints:
        for i, hint in enumerate(hints, 1):
            show_hint(hint, f"Hint {i}", context=f"Try this if you're stuck (hint {i} of {len(hints)})")
    
    # Show common mistakes if provided
    if common_mistakes:
        mistakes_html = ""
        for mistake in common_mistakes:
            mistakes_html += f"<li style='margin: 5px 0;'>{_format_message(mistake)}</li>"
        
        display(HTML(f"""
        <div style='background-color: #ffebee; padding: 15px; margin: 10px 0; 
                    border-radius: 5px; border-left: 6px solid #f44336;'>
            <h4 style='margin: 0 0 10px 0; color: #c62828;'>⚠️ Common Mistakes to Avoid:</h4>
            <ul style='margin: 0; padding-left: 20px; color: #666;'>
                {mistakes_html}
            </ul>
        </div>
        """))