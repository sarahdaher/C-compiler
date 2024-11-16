# Structure de l'AST

## Types des *types*

- `int`

- `void`

- `char`

- `pointer`
  - `sub_type` : *type* du pointeur

- `tab` : tableau de taille connue
  - `sub_type` : *type* des éléments du tableau
  - `size` : taille du tableau

## Types des définitions globales

- `def_var_global` : déclaration d'une variable globale
  - `type` : *type* de la variable
  - `name` : nom de la variable  

- `def_fun` : déclaration d'une fonction
  - `type` : *type* de la valeur de retour
  - `name` : nom de la fonction
  - `args` : tableau des arguments de la fonction
    - `type` : *type* de l'argument
    - `name` : nom de l'argument
  - `body` : liste de *statements*

## Actions des *statements*

- `return` : renvoie une expression
  - `value` : *expression* à renvoyer

- `call` : appel une fonction
  - `name` : nom de la fonction
  - `args` : liste d'*expressions* correspondant aux arguments

- `def_var_local` : déclaration d'une variable local
  - `type` : *type* de la variable
  - `name` : nom de la variable

- `var_set` : affectation d'une expression à une variable
  - `left_value` : nom de la variable
  - `value` : *expression* à affecter

- `def_var_local_set` : déclaration d'une variable local et affectation d'une expression
  - `type` : *type* de la variable
  - `name` : nom de la variable
  - `value` : *expression* à affecter

- `block` : bloc de statements
  - `statements` : liste des *statements*

- `if_else` : branche conditionnelle
  - `condition` : *expression* de la condition
  - `then_body` : *statement* à exécuter si la condition est vraie
  - `else_body` : *statement* à exécuter si la condition est fausse

- `while` : boucle tant que
  - `condition` : *expression* de la condition
  - `body` : *statement* à exécuter tant que la condition est vraie

- `break` : arrête une boucle

- `continue` : passe à l'itération suivante de la boucle

## Types des *valeurs gauches (left values)*

- `variable`
  - `name` : nom de la variable

- `dereference` : déréférence d'une valeur gauche
  - `address` : *expression* qui représente l'adresse à déférencer

## Types des *expressions*

- `integer` : entier constant
  - `value`

- `char` : caractère constant
  - `value`

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

- `equal` : égalité entre deux expressions
  - `left` : *expression* de gauche
  - `right` : *expression* de droite

- `non_equal` : non égalité entre deux expressions
  - `left` : *expression* de gauche
  - `right` : *expression* de droite

- `less` : comparaison inférieur stricte entre deux expressions
  - `left` : *expression* de gauche
  - `right` : *expression* de droite

- `less_equal` : comparaison inférieur entre deux expressions
  - `left` : *expression* de gauche
  - `right` : *expression* de droite

- `greater` : comparaison supérieur stricte entre deux expressions
  - `left` : *expression* de gauche
  - `right` : *expression* de droite

- `greater_equal` : comparaison supérieur entre deux expressions
  - `left` : *expression* de gauche
  - `right` : *expression* de droite

- `and` : et logique entre deux expressions
  - `left` : *expression* de gauche
  - `right` : *expression* de droite

- `or` : ou logique entre deux expressions
  - `left` : *expression* de gauche
  - `right` : *expression* de droite

- `not` : négation d'une expression
  - `value` : *expression* à négliger

- `call` : appel d'une fonction
  - `name` : nom de la fonction
  - `args` : argument de la fonction qui est une *expression*

- `tab` : tableau explicite
  - `elements` : liste des *expressions*

- `val` : référence à une valeur gauche
  - `left_value` : *left value* à référencer

- `reference` : référence d'une valeur gauche
  - `left_value` : *left value* à référencer

- `sizeof` : taille d'un type
  - `typee` : *type* pour lequel obtenir la taille

- `convert_to_pointer` : passe d'une taille quelconque à la taille d'un pointeur
  - `value` : *expression* à redimensionner

- `convert_to_int` : passe d'une taille quelconque à la taille d'un entier
  - `value` : *expression* à redimensionner

- `string` : chaîne de caractères
  - `value` : la chaîne de caractères
