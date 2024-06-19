def get_form_template():
    return """
    <style>
        .form-label {{
            font-size: 1.2em;
            color: #555;
        }}
        .form-select {{
            width: 100%;
            height: 35px;
            padding: 5px;
            border-radius: 5px;
            border: 1px solid #ccc;
            font-size: 1em;
            color: #333;
        }}
    </style>
    <label for="server" class="form-label">Select your server</label>
    <select name="server" size="1" class="form-select">
        {options}
    </select>
    """
