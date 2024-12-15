from fasthtml.common import *

# Define document type
doc = DOCTYPE("html")

# Define page content
page = html(
    lang="en-US",
    head=head(
        meta(charset="utf-8"),
        title="James Clerk Maxwell",
    ),
    body=body(
        h1("James Clerk Maxwell (1831-1879)"),
        p(
            img(
                src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/James-Clerk-Maxwell-1831-1879.jpg/330px-James-Clerk-Maxwell-1831-1879.jpg",
                alt="James-Clerk-Maxwell-1831-1879",
                width=230,
                height=280,
            )
        ),
        p(
            "James Clerk Maxwell FRS FRSE (13 June 1831 – 5 November 1879) was a Scottish physicist and mathematician who was responsible for the classical theory of electromagnetic radiation, which was the first theory to describe electricity, magnetism and light as different manifestations of the same phenomenon. Maxwell's equations for electromagnetism have been called the 'second great unification in physics' where the first one had been realised by Isaac Newton."
        ),
        p(
            "Einstein, when he visited the University of Cambridge in 1922, was told by his host that he had done great things because he stood on Newton's shoulders; Einstein replied: 'No I don't. I stand on the shoulders of Maxwell.'"
        ),
        p(
            "Electricity and magnetism are my worst subjects in physics. Maxwell described the relationship between electricity and magnetism in four simple partial differential equations. Even though the equations are simple in form, I still don’t understand them. I am in awe of someone so brilliant."
        ),
        p(
            img(src="./img/maxwell_equations.PNG", alt="Maxwell Equations", width=150, height=100)
        ),
        a(href="https://en.wikipedia.org/wiki/James_Clerk_Maxwell", text="James-Clerk-Maxwell"),
    ),
)

# Render the final HTML
print(render(doc, page))
