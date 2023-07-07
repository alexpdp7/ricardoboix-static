import subprocess

import htmlgenerator as h


def template(title="title", selected_tab=None, id=None):
    tabs = {
        "Home": "index.html",
        "Galería de arte": "galeria.html",
        "Poesías": "poesias.html",
        "Relatos": "relatos.html",
        "Canciones": "canciones.html",
        "Libro de visitas": "librodevisitas.html",
    }

    menu_lis = [
        h.LI(
            h.A(
                tab,
                href=link,
            ),
            role="presentation",
            _class="active" if selected_tab == tab else None,
        )
        for tab, link in tabs.items()
    ]
    return h.HTML(
        h.HEAD(
            h.TITLE(title),
            h.LINK(href="https://fonts.googleapis.com/css?family=Mr+Dafoe", rel="stylesheet"),
            h.LINK(href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css", rel="stylesheet"),
            h.LINK(href="estilo.css", rel="stylesheet", media="screen"),
            h.SCRIPT(src="http://code.jquery.com/jquery-1.11.1.min.js"),
            h.SCRIPT(src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/js/bootstrap.min.js"),
        ),
        h.BODY(
            h.DIV(
                h.DIV(
                    h.DIV(
                        h.UL(
                            *menu_lis,
                            _class="nav nav-tabs",
                        ),
                        _class="col-md-12",
                    ),
                    _class="row",
                ),
                _class="container",
            ),
            h.DIV("Ricardo Boix", id="titulo"),
        ),
        doctype="html",
        id=id,
    )


def tidy(s):
    p = subprocess.run(["tidy", "--indent", "yes", "-q", "-wrap", "160"], input=s, stdout=subprocess.PIPE, encoding="UTF8")
    return p.stdout


with open("index.html", "w") as f:
    f.write(tidy(h.render(template(title="Ricardo Boix", selected_tab="Home", id="portada"), {})))

