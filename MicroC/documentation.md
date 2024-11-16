# Types des définitions globales

- `def_var_global` : déclaration d'une variable globale
  - `name` : nom de la variable  

- `def_fun` : déclaration d'une fonction
  - `name` : nom de la fonction
  - `arg` : nom de l'argument
  - `body` : liste de *statements*

# Actions des *statements*

- `print` : affiche une expression
  - `value` : *expression* à afficher

- `read` : lit un entier
  - `name` : nom de la variable dans laquelle mettre la valeur lut

- `return` : renvoie une expression
  - `value` : *expression* à renvoyer

- `call` : appel une fonction
  - `name` : nom de la fonction
  - `value` : argument de la fonction qui est une *expression*

- `def_var_local` : déclaration d'une variable local
  - `name` : nom de la variable

- `var_set` : affectation d'une expression à une variable
  - `name` : nom de la variable
  - `value` : *expression* à affecter

- `def_var_local_set` : déclaration d'une variable local et affectation d'une expression
  - `name` : nom de la variable
  - `value` : *expression* à affecter

# Types des *expressions*

- `cst` : valeur constante
  - `value` : valeur de la constante

- `add` : addition
  - `left` : *expression* de gauche
  - `right` : *expression* de droite

- `sub` : soustraction
  - `left` : *expression* de gauche
  - `right` : *expression* de droite

- `mul` : multiplication
  - `left` : *expression* de gauche
  - `right` : *expression* de droite

- `div` : division entière
  - `left` : *expression* de gauche
  - `right` : *expression* de droite

- `mod` : reste de la division entière
  - `left` : *expression* de gauche
  - `right` : *expression* de droite

- `call` : appel d'une fonction
  - `name` : nom de la fonction
  - `value` : argument de la fonction qui est une *expression*

- `var_get` : valeur d'une variable
  - `name` : nom de la variable
