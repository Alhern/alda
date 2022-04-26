#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class AldaExecute:

    def __init__(self, tree, env):
        self.env = env
        result = self.eval_node(tree)

        if result is not None and isinstance(result, int):
            print(result)
        if isinstance(result, str):
            print(result)
        if isinstance(result, float):
            print(result)

    def eval_node(self, node):

        if isinstance(node, float):
            return node
        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node

        if node is None:
            return None

        if node[0] == 'nombre_flottant':
            return node[1]

        if node[0] == 'nombre':
            return node[1]

        if node[0] == 'chaine':
            return node[1]

        if node[0] == 'liste_stat':
            res = []
            for i in range(1, len(node)):
                res.append(self.eval_node(node[i]))
            return res

        # ARITHMETIQUE

        if node[0] == 'plus':
            return self.eval_node(node[1]) + self.eval_node(node[2])
        elif node[0] == 'moins':
            return self.eval_node(node[1]) - self.eval_node(node[2])
        elif node[0] == 'fois':
            return self.eval_node(node[1]) * self.eval_node(node[2])
        elif node[0] == 'divise':
            return self.eval_node(node[1]) // self.eval_node(node[2])
        elif node[0] == 'mod':
            return self.eval_node(node[1]) % self.eval_node(node[2])

        # OPERATEURS DE COMPARAISON

        if node[0] == 'egal':
            return self.eval_node(node[1]) == self.eval_node(node[2])
        if node[0] == 'negal':
            return self.eval_node(node[1]) != self.eval_node(node[2])
        if node[0] == 'pgr':
            return self.eval_node(node[1]) > self.eval_node(node[2])
        if node[0] == 'mgr':
            return self.eval_node(node[1]) < self.eval_node(node[2])
        if node[0] == 'pegr':
            return self.eval_node(node[1]) >= self.eval_node(node[2])
        if node[0] == 'megr':
            return self.eval_node(node[1]) <= self.eval_node(node[2])

        # CONDITIONS

        if node[0] == 'si':
            if (
                    len(node) == 3):  # si on a un seul ordre dans la commande (càd pas de SINON), on évalue la
                # condition et on ne retourne rien si elle est fausse :
                if self.eval_node(node[1]):
                    return self.eval_node(node[2])
                else:
                    return
            else:  # si on a un SINON dans la commande, on l'évalue :
                if self.eval_node(node[1]):
                    return self.eval_node(node[2])
                if node[3]:
                    return self.eval_node(node[3])
                else:
                    return

        # OPERATEURS LOGIQUES

        if node[0] == 'et':
            return self.eval_node(node[1]) and self.eval_node(node[2])

        if node[0] == 'ou':
            return self.eval_node(node[1]) or self.eval_node(node[2])

        # FONCTION

        if node[0] == 'fo_def':
            self.env[node[1]] = node[2]

        if node[0] == 'fo_appel':
            try:
                return self.eval_node(self.env[node[1]])
            except LookupError:
                print(f"Fonction indéfinie : {node[1]}")
                return

        # BOUCLES

        if node[0] == 'tantque':
            condition = self.eval_node(node[1])
            while condition:
                self.eval_node(node[2])
                condition = self.eval_node(node[1])

        if node[0] == 'de':
            for i in range(self.eval_node(node[1]), self.eval_node(node[2])):
                self.eval_node(node[3])

        # VARIABLES

        if node[0] == 'var_assigne':
            self.env[node[1]] = self.eval_node(node[2])
            return node[1]

        if node[0] == 'nom':
            try:
                return self.env[node[1]]
            except LookupError:
                print(f"Nom indéfini : '{node[1]}'")
                return 0

        if node[0] == 'ecris':
            print(self.eval_node(node[1]))
            return node[1]

        # LISTE

        if node[0] == 'liste_elem':
            if node[1][0] == 'nom' and node[2][0] == 'nom':
                return '%s, %s' % (node[1][1], node[2][1])
            if node[1][0] == 'nom':  # en faisant ça on évite d'afficher la valeur
                return '%s, %s' % (node[1][1], self.eval_node(node[2]))
            if node[2][0] == 'nom':
                return '%s, %s' % (self.eval_node(node[1]), node[2][1])
            else:
                return '%s, %s' % (self.eval_node(node[1]), self.eval_node(node[2]))

        if node[0] == 'liste':
            return '[%s]' % (self.eval_node(node[1]))
