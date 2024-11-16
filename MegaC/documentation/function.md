# Appels de fonctions

## Problèmes d'alignements

Quand on appelle les fonctions de la libc, `%rsp` doit être un multiple de 16.
C'est pour cela que l'on appelle `_check_align` à chaque fois que l'on appelle
une fonction de la libc : c'est un garde-fou contre les problèmes d'alignements
qui nous permet de savoir si l'erreur de segmentation est une erreur liée à
l'alignement ou à une autre erreur.

On a décidé que même pour les autres fonctions (c'est-à-dire les fonctions
créées par l'utilisateur) que l'on alignerait `%rsp` sur 16 à chaque appel.
C'est pour cela que l'on ajoute un offset avant chaque appel.

## Ordre des arguments

Les 14 premiers arguments de l'appel sont stockés dans les registres :
- `%rax`
- `%rbx`
- `%rcx`
- `%rdx`
- `%rsi`
- `%rdi`
- `%r8`
- `%r9`
- `%r10`
- `%r11`
- `%r12`
- `%r13`
- `%r14`
- `%r15`
Ensuite les autres arguments sont stockés sur la pile avant l'appel de la
fonction dans l'ordre décroissant des adresses.

## Structure de la pile

### Fonction à moins de 14 arguments

Imaginons que l'on appelle `g` qui prend `n` arguments (inférieur ou égal à 14)
dans une fonction `f`.
 
```
+-------------------+ <- %rbp de f
| var locale 1      |
+-------------------+
| var locale 2      |
+-------------------+
| ...               |
+-------------------+
| var locale 3      |
+-------------------+
| offset            |
+-------------------+ <- début de l'appel
| adresse de retour |
+-------------------+
| %rbp de f         |
+-------------------+ <- %rbp de g
| argument 1        |
+-------------------+
| argument 2        |
+-------------------+
| ...               |
+-------------------+
| argument n        |
+-------------------+
```

### Fonction à plus de 15 arguments

Imaginons que l'on appelle `g` qui prend `n` arguments dans une fonction `f`.

```
+-------------------+ <- %rbp de f
| var locale 1      |
+-------------------+
| var locale 2      |
+-------------------+
| ...               |
+-------------------+
| var locale 3      |
+-------------------+ on ajoute l'offset avant les arguments pour que les
| offset            | arguments soient toujours à la même place par rapport
+-------------------+ au %rbp de g
| argument 15       |
+-------------------+
| argument 16       |
+-------------------+
| ...               |
+-------------------+ <- %rbp de g + 16 + sizeof(arg(n))
| argument n        |
+-------------------+ <- début de l'appel | %rbp de g + 16
| adresse de retour |
+-------------------+
| %rbp de f         |
+-------------------+ <- %rbp de g
| argument 1        |
+-------------------+
| argument 2        |
+-------------------+
| ...               |
+-------------------+
| argument 14       |
+-------------------+
```
