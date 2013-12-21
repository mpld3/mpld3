BUTTON_TEMPLATE = """
<button class="mpld3_button" id='button{figid}' onclick="open_figured{figid}()">Open in a new window</button>
"""

BUTTON_SCRIPT = """
    <script  type="text/javascript">
      function open_figured{figid}()
      {{
        window.open("file://{fig_url_new_window}",
                    "_blank",
                    "toolbar=no, scrollbars=yes, resizable=yes, top=100, left=100, width={width}, height={height}, titlebar=no, menubar=no, location=yes");
      }}
    </script>
"""

BUTTON_STYLE = """
    <style>

    .mpld3_button {
      overflow: visible;
      display: inline-block;
      padding: 0.5em 1em;
      border: 1px solid #d4d4d4;
      margin: 0;
      text-decoration: none;
      text-shadow: 1px 1px 0 #fff;
      font: 100%/normal sans-serif;
      color: #333;
      white-space: nowrap;
      cursor: pointer;
      outline: none;
      background-color: #ececec;
      background-image: -webkit-gradient(linear, 0 0, 0 100%, from(#f4f4f4), to(#ececec));
      background-image: -moz-linear-gradient(#f4f4f4, #ececec);
      background-image: -o-linear-gradient(#f4f4f4, #ececec);
      background-image: linear-gradient(#f4f4f4, #ececec);
      -webkit-background-clip: padding;
      -moz-background-clip: padding;
      -o-background-clip: padding-box;
      background-clip: padding-box;
      -webkit-border-radius: 0.2em;
      -moz-border-radius: 0.2em;
      border-radius: 0.2em;
      zoom: 1;
    }

    .mpld3_button:hover,
    .mpld3_button:focus,
    .mpld3_button:active {
      border-color: #3072b3;
      border-bottom-color: #2a65a0;
      text-decoration: none;
      text-shadow: -1px -1px 0 rgba(0,0,0,0.3);
      color: #fff;
      background-color: #3072b3;
      background-image: -webkit-gradient(linear, 0 0, 0 100%, from(#599bdc), to(#3072b3));
      background-image: -moz-linear-gradient(#599bdc, #3072b3);
      background-image: -o-linear-gradient(#599bdc, #3072b3);
      background-image: linear-gradient(#599bdc, #3072b3);
      }
    </style>
"""
