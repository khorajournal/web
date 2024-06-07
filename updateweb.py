import sys
import json

valid_help_flags = [
    "h",
    "-h",
    "--h",
    "help",
    "-help",
    "--help",
]
def gen_header(htitle, stylepath):
    return f'''<html><head><title>{htitle}</title>\n<link rel="stylesheet" href="{stylepath}">\n<script type="module" src="https://md-block.verou.me/md-block.js"></script></head>\n<body>\n'''

def gen_h1(content):
    return f'''<h1>{content}</h1>'''

def gen_tail():
    return f'''</body></html>\n'''

def gen_p(content):
    return f'''<p>{content}</p>\n'''

def link_to_view(nlink):
    return nlink.split(".html")[0].split("/")[-1]

def gen_navbar(nav_links):
    lis = '\n'.join([f'''<li><a href="''' + nav_link + f'''">''' + link_to_view(nav_link) + f'''</a></li>''' for nav_link in nav_links])
    return f'''<ul>''' + lis + f'''</ul>'''

def gen_img(path, style=None):
    if style == None:
        return f'''<img src="''' + path + f'''">\n'''
    else:
        return f'''<img class="{style}" src="{path}">\n'''

def start_div(style):
    if style == None:
        return f'''<div>\n'''
    else:
        return f'''<div class="''' + style + f'''">\n''' 

def gen_mdblock(mdpath):
    with open(mdpath, "r") as mdin:
        mdpayload = mdin.read()

    return f'''<md-block>{mdpayload}</md-block>'''

def end_div():
    return f'''</div>\n'''

def construct_css(config):

    # Accessing the data
    css_filepath = config['css_config']['filepath']

    body_font = config['css_config']['body_style']['font-family']

    p_align = config['css_config']['p_style']['p_align']
    p_fontsize = config['css_config']['p_style']['p_fontsize']
    p_margin_left = config['css_config']['p_style']['margin-left']
    p_margin_right = config['css_config']['p_style']['margin-right']

    h1_align = config['css_config']['h1_style']['text-align']

    div_width = config['css_config']['div_style']['width']
    div_padding = config['css_config']['div_style']['padding']
    div_margin = config['css_config']['div_style']['margin']

    navbar_color = config['css_config']['navbar_style']['background_color']
    navbar_height = config['css_config']['navbar_style']['height']


    bannerimg_display = config['css_config']['bannerimg_style']['display']
    bannerimg_margin_left = config['css_config']['bannerimg_style']['margin-left']
    bannerimg_margin_right = config['css_config']['bannerimg_style']['margin-right']
    bannerimg_width = config['css_config']['bannerimg_style']['width']
    bannerimg_height = config['css_config']['bannerimg_style']['height']

    def style_body(body_font):
        return f'''
body {{
    font-family: {body_font}
}}
                '''

    def style_p(palign, pfontsize, p_margin_left, p_margin_right):
        return f'''
p {{
    text-align: {palign};
    font-size: {pfontsize};
    margin-left: {p_margin_left};
    margin-right: {p_margin_right};
}}

                '''
    def style_h1(text_align):
        return f'''
h1 {{
    text-align: {text_align}
}}
                '''

    def style_div(div_width, div_padding, div_margin):
        return f'''
div {{
    width: {div_width};
    padding: {div_padding};
    margin: {div_margin};

}}

            '''

    def style_navbar(bcolor, bheight):
        return f'''
ul {{
    list-style-type: none;
    margin: 0;
    padding: 0;
    background-color: {bcolor};
    height: {bheight};
}}

li {{
    display: inline;
    height: 100%;
    margin: auto;
}}

li + li {{
    margin : 1em;
}}

div.navbardiv {{
    margin: auto;
}}

            '''

    def style_bannerimg(bannerimg_display, bannerimg_margin_left, bannerimg_margin_right, bannerimg_width, bannerimg_height):
        return f'''
.bannerimg {{
    display: {bannerimg_display};
    margin-left: {bannerimg_margin_left};
    margin-right: {bannerimg_margin_right};
    width: {bannerimg_width};
    height: {bannerimg_height};

}}

                '''
    
    #Construct CSS Payload
    css_payload = ""
    css_payload += style_body(body_font)
    css_payload += style_p(p_align, p_fontsize, p_margin_left, p_margin_right)
    css_payload += style_h1(h1_align)
    css_payload += style_div(div_width, div_padding, div_margin)
    css_payload += style_navbar(navbar_color, navbar_height)
    css_payload += style_bannerimg(bannerimg_display, bannerimg_margin_left, bannerimg_margin_right, bannerimg_width, bannerimg_height)
    
    #Deliver Payload to Filesystem
    with open(css_filepath, "w") as css_out:
        css_out.write(css_payload)


def construct_pages(config):
    
    template_map = config['pages_config']['page_template_types']
    page_titles = config['pages_config']['manifest']
    page_templates = config['pages_config']['page_templates']

    for entry, page_type in page_titles.items():
        page_config = page_templates[template_map[page_type]]
        page_html = ""
        page_html += gen_header(entry, page_config['style_path'])
        page_html += gen_h1(entry)
        page_html += start_div(style=None)
        page_html += gen_mdblock("./include/markdown/" + entry + "_bannertext.md")
        page_html += end_div()
        page_html += gen_tail()
        
        with open("./include/pages/" + entry + ".html", "w") as page_out:
            page_out.write(page_html)

def construct_index(config):

    # Accessing the data
    index_filepath = config['index_config']['filepath']
    page_title = config['index_config']['page_title']
    navbar_filepath = config['index_config']['navbar_path']
    bannerimg_filepath = config['index_config']['bannerimg_path']
    bannertext_filepath = config['index_config']['bannertext_path']
    page_titles = config['pages_config']['manifest']

    style_path = config['css_config']['filepath']

    indexstr = ""
    indexstr += gen_header(page_title, style_path)
    indexstr += start_div(style="navbardiv")
    indexstr += gen_navbar(["./include/pages/" + t + ".html" for t in list(page_titles.keys())])
    indexstr += end_div() 
    indexstr += gen_h1(page_title)
    indexstr += start_div(style=None)
    indexstr += gen_img(bannerimg_filepath, style="bannerimg") 
    #indexstr += gen_p("We first find the Khora in the Timaeaus which seems to be oriented around the question of the topos or place of Being")
    indexstr += gen_mdblock(bannertext_filepath)
    indexstr += end_div()
    indexstr += gen_tail()

    with open(index_filepath, "w") as index_out:
        index_out.write(indexstr)


########################################################
#IGNITION
########################################################

#Load the config file (may have changes)
with open(sys.argv[1], 'r') as file:
    config_data = json.load(file)
#Load the old config file
with open('snapshots/' + sys.argv[1]) as old_snapshot:
    old_snapshot_data = json.load(old_snapshot)
#only change the website if there is a change
#TODO: make logic more complicated
#Amortized Runtime is not good enough in event of structural advesarial tendencies
if old_snapshot_data != config_data:

    construct_css(config_data)
    construct_pages(config_data)
    construct_index(config_data)

    #save snapshot
    with open(sys.argv[1], "r") as new_config:
        configstr = new_config.read()
    with open('snapshots/' + sys.argv[1], "w") as snapshot:
        snapshot.write(configstr)
