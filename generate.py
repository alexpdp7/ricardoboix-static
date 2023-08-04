import itertools
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
            h.LINK(href="/estilo.css", rel="stylesheet", media="screen"),
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

    audio_element = None
    last_line = poem.splitlines()[-1]
    if last_line.startswith("audio:"):
        audio = last_line[len("audio:"):]
        poem = poem[:poem.find("audio:")]
        audio_element = h.IFRAME(
            width="100%",
            height="166",
            scrolling="no",
            frameborder="no",
            style="text-align: center; margin-top: 3em;",
            src=f"https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/{audio}&amp;color=ff5500&amp;auto_play=false&amp;hide_related=false&amp;show_comments=true&amp;show_user=true&amp;show_reposts=false",
        )

    poem_html = markdown.markdown(poem)
    title = pathlib.Path(path).stem
    html_path = pathlib.Path("poesias") / title
    html_path = html_path.with_suffix(".html")

    extra_container_contents = [h.H2(title)]
    if audio_element is not None:
        extra_container_contents.append(audio_element)
    extra_container_contents += [
        h.DIV(
            h.mark_safe(poem_html),
            id="textopoesia",
        ),
        h.DIV(
            h.A(
                "Volver a Poesías",
                href="/poesias.html",
                _class="btn btn-default active",
                role="button"
            ),
            id="button",
        ),
    ]

    with open(html_path, "w") as f:
        f.write(tidy(h.render(template(
            title=f"Ricardo Boix - Poesías - {pathlib.Path(path).stem}",
            selected_tab=None,
            id="bodylibro",
            content=None,
            extra_container_contents=extra_container_contents,
        ), {})))


with open("relatos.html", "w") as f:
    relatos = [
        h.P(
            h.A(
                titulo,
                href=f"relatos/{titulo}.html"
            ),
            style="text-align: center",
        )
        for titulo in map(lambda p: p.stem, sorted(pathlib.Path("relatos_md").glob("*.md")))
    ]
    extra_container_contents = [
        h.DIV(
            h.BR(),
            h.BR(),
            h.BR(),
            h.BR(),
            h.BR(),
            h.BR(),
            h.BR(),
            h.BR(),
            h.DIV(
                *relatos,
            ),
        ),
        h.IMG(
            id="indicerelatos",
            src="skyline.png",
        ),
    ]

    f.write(tidy(h.render(template(
        title="Ricardo Boix - Relatos",
        selected_tab="Relatos",
        content=None,
        extra_container_contents=extra_container_contents,
    ), {})))

pathlib.Path("relatos").mkdir(exist_ok=True)

for path in pathlib.Path("relatos_md").glob("*.md"):
    with open(path) as relato_file:
        relato = relato_file.read()

    relato_html = markdown.markdown(relato)
    title = pathlib.Path(path).stem
    html_path = pathlib.Path("relatos") / title
    html_path = html_path.with_suffix(".html")

    extra_container_contents = [h.H2(title)]
    extra_container_contents += [
        h.DIV(
            h.mark_safe(relato_html),
            id="textorelato",
        ),
        h.DIV(
            h.A(
                "Volver a Relatos",
                href="/relatos.html",
                _class="btn btn-default active",
                role="button"
            ),
            id="button",
        ),
    ]

    with open(html_path, "w") as f:
        f.write(tidy(h.render(template(
            title=f"Ricardo Boix - Relatos - {pathlib.Path(path).stem}",
            selected_tab=None,
            content=None,
            extra_container_contents=extra_container_contents,
        ), {})))


with open("canciones.html", "w") as f:
    playlists = [
        ("Tangos", 337001614),
        ("Boleros", 337008899),
        ("Varios", 337009203),
    ]

    def playlist_to_html(playlist):
        title, id = playlist
        return [
            h.H2(title),
            h.DIV(
                h.IFRAME(
                    width="50%",
                    height="400",
                    scrolling="no",
                    frameborder="no",
                    src=f"https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/playlists/{id}&amp;auto_play=false&amp;hide_related=false&amp;show_comments=true&amp;show_user=true&amp;show_reposts=false&amp;visual=true",
                ),
            ),
            h.BR(),
        ]

    extra_container_contents = h.DIV(
        h.BR(),
        h.BR(),
        h.DIV(
            *itertools.chain(*map(playlist_to_html, playlists)),
            _class="col-md-8",
        ),
        _class="row",
    )

    f.write(tidy(h.render(template(
        title="Ricardo Boix - Canciones",
        selected_tab="Canciones",
        id="bodylibro",
        content=None,
        extra_container_contents=[extra_container_contents],
    ), {})))
