import pathlib
import subprocess

import markdown
import htmlgenerator as h


def template(content, title="title", selected_tab=None, id=None, extra_container_contents=[]):
    container_contents = []

    if selected_tab:
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

        container_contents.append(
            h.DIV(
                h.DIV(
                    h.UL(
                        *menu_lis,
                        _class="nav nav-tabs",
                    ),
                    _class="col-md-12",
                ),
                _class="row",
            )
        )

    container_contents += extra_container_contents

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
                *container_contents,
                _class="container",
            ),
            content,
        ),
        doctype="html",
        id=id,
    )


def tidy(s):
    p = subprocess.run(["tidy", "--indent", "yes", "-q", "-wrap", "160"], input=s, stdout=subprocess.PIPE, encoding="UTF8")
    return p.stdout


with open("index.html", "w") as f:
    f.write(tidy(h.render(template(
        title="Ricardo Boix",
        selected_tab="Home",
        id="portada",
        content=h.DIV("Ricardo Boix", id="titulo"),
    ), {})))

with open("galeria.html", "w") as f:
    links = [
        h.A(
            h.IMG(
                alt=f"Cuadro {i}",  # TODO
                src=f"foto/{i}.jpg",
                _class="cuadro",
            ),
            href=f"foto/{i}.jpg",
        )
        for i in range(1, 61)
    ]
    extra_container_contents = h.DIV(
        h.BR(),
        h.BR(),
        h.DIV(
            *links,
            _class="col-md-12",
        ),
        _class="row",
    )
    f.write(tidy(h.render(template(
        title="Ricardo Boix - Galería de arte",
        selected_tab="Galería de arte",
        id="galeria",
        content=None, # h.DIV("Ricardo Boix", id="titulo"),
        extra_container_contents=[extra_container_contents],
    ), {})))

with open("poesias.html", "w") as f:
    def _p(path: pathlib.Path):
        with open(path) as f:
            has_audio = "audio:" in f.read()

        text = path.stem
        if has_audio:
            text += " (audio)"
        return (path.stem, text)
    poesias = [
        h.P(
            h.A(
                text,
                href=f"poesias/{titulo}.html"
            ),
            style="text-align: center",
        )
        for (titulo, text) in map(_p, sorted(pathlib.Path("poemas").glob("*.md")))
    ]
    extra_container_contents = h.DIV(
        h.BR(),
        h.BR(),
        h.DIV(
            h.BR(),
            h.BR(),
            h.DIV(
                h.IMG(src="adorno_l.png"),
                h.IMG(src="adorno_l.png"),
                _class="desktop hidden-xs hidden-sm",
            ),
            _class="col-md-2",
        ),
        h.DIV(
            *poesias,
            _class="col-md-8",
        ),
        h.DIV(
            h.BR(),
            h.BR(),
            h.DIV(
                h.IMG(src="adorno_r.png"),
                h.IMG(src="adorno_r.png"),
                _class="desktop hidden-xs hidden-sm",
            ),
            _class="col-md-2",
        ),
        _class="row",
    )

    f.write(tidy(h.render(template(
        title="Ricardo Boix - Poesías",
        selected_tab="Poesías",
        id="bodylibro",
        content=None,
        extra_container_contents=[extra_container_contents],
    ), {})))

pathlib.Path("poesias").mkdir(exist_ok=True)

for path in pathlib.Path("poemas").glob("*.md"):
    with open(path) as poem_file:
        poem = poem_file.read()
    poem_html = markdown.markdown(poem)
    title = pathlib.Path(path).stem
    html_path = pathlib.Path("poesias") / title
    html_path = html_path.with_suffix(".html")
    with open(html_path, "w") as f:
        f.write(tidy(h.render(template(
            title=f"Ricardo Boix - Poesías - {pathlib.Path(path).stem}",
            selected_tab=None,
            id="bodylibro",
            content=None,
            extra_container_contents=[
                h.H2(title),
                h.mark_safe(poem_html),
            ],
        ), {})))
