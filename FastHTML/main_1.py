# https://github.com/AnswerDotAI/fasthtml
# https://about.fastht.ml/
# https://levainbakery.com/


from fasthtml.common import *

app, rt = fast_app()
clicks = 0

@rt('/')
def get():
    clicks_count = result(clicks)
    # return Div(P(clicks_count), hx_get="/change", hx_target="this")
    return my_html  

@rt('/change')
def change():
    global clicks  # Access the global clicks variable
    clicks += 1  
    clicks_count = result(clicks)
    return Div(P(clicks_count))

def result(clicks):
    msg_click_count = f"Hello World!, click count = {clicks} is {'even' if clicks % 2 == 0 else 'odd'}."
    return msg_click_count 



my_html =
  <p>  
  <head>
    <meta charset="utf-8" />
    <title>James Clerk Maxwell</title>
  </head>

  <body>
    <h1>
      James Clerk Maxwell (1831-1879)
    </h1>
    <p>
      <img 
        src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/James-Clerk-Maxwell-1831-1879.jpg/330px-James-Clerk-Maxwell-1831-1879.jpg"
        alt="James-Clerk-Maxwell-1831-1879" 
        width="230" 
        height="280"
      />
    </p>
    <p>
      James Clerk Maxwell FRS FRSE (13 June 1831 to 5 November 1879) was 
      a Scottish physicist and mathematician who was responsible for 
      the classical theory of electromagnetic radiation, which was 
      the first theory to describe electricity, magnetism and light 
      as different manifestations of the same phenomenon. 
      Maxwell's equations for electromagnetism have been called 
      the "second great unification in physics" where the 
      first one had been realised by Isaac Newton. 
    </p>
    <p>
      Einstein, when he visited the University of Cambridge in 1922, 
      was told by his host that he had done great things because he stood on Newton's shoulders; 
      Einstein replied: "No I don't. I stand on the shoulders of Maxwell."
    </p>    
    <p>
      Electricity and magnetism are my worst subjects in physics. 
      Maxwell described the relationship between electricity and magnetism in four 
      simple partial differential equations.
      Even though the equations are simple in form, 
      I still don’t understand them. I am in awe of someone so brilliant.      
    </p>
    <p>
      <img 
        src="./img/maxwell_equations.PNG"
        alt="Maxwell Equations"
        width="150"
        height="100"
      />
    </p>
    <a href="https://en.wikipedia.org/wiki/James_Clerk_Maxwell">James-Clerk-Maxwell</a>  
    </body>
    </p>






serve()