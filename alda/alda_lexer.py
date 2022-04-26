#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sly import Lexer


class AldaLexer(Lexer):
    tokens = {NOM, NOMBRE, NOMBRE_FLOTTANT, ECRIS,
              CHAINE, PLUS, MOINS, FOIS,
              DIVISE, MOD, EGAL, NEGAL, PGR,
              MGR, PEGR, MEGR, EST,
              SI, ALORS, SINON, TANTQUE,
              FAIS, DE, JUSQUA, ET,
              OU, CGAU, CDRO, PGAU,
              PDRO, VIRGULE, VRAI, FAUX,
              INCR, DECR, PVIRG, FO,
              DPTS}

    ignore = ' \t'

    literals = {'+', '-', '*', '/', '==', '!=', '>', '<', '>=', '<=', '=', '[', ']', '(', ')', '{', '}', ';'}

    ECRIS = r'ECRIS'
    PLUS = r'\+'
    MOINS = r'-'
    FOIS = r'\*'
    DIVISE = r'/'
    MOD = r'%'
    PEGR = r'>=(?!=)'
    MEGR = r'<=(?!=)'
    EGAL = r'(?<!=)={2}(?!=)'
    NEGAL = r'!=(?!=)'
    PGR = r'>'
    MGR = r'<'
    EST = r'(?<!=)=(?!=)'
    CGAU = r'\['
    CDRO = r'\]'
    PGAU = r'\('
    PDRO = r'\)'
    VIRGULE = r','
    PVIRG = r';'
    DPTS = r':'

    SINON = r'SINON'
    SI = r'SI'
    ALORS = r'ALORS'
    TANTQUE = r'TANTQUE'
    FO = r'FO'
    FAIS = r'FAIS'
    DE = r'DE'
    JUSQUA = r'JUSQUA'
    ET = r'ET'
    OU = r'OU'
    VRAI = r'VRAI'
    FAUX = r'FAUX'
    INCR = r'INCR'
    DECR = r'DECR'

    NOM = r'[a-zA-Z_][a-zA-Z0-9_]*'

    CHAINE = r"(\"[^\"]*\")|('[^']*')"

    NOM['sinon'] = SINON
    NOM['si'] = SI
    NOM['alors'] = ALORS
    NOM['tantque'] = TANTQUE
    NOM['fo'] = FO
    NOM['fais'] = FAIS
    NOM['de'] = DE
    NOM['jusqua'] = JUSQUA
    NOM['incr'] = INCR
    NOM['decr'] = DECR
    NOM['et'] = ET
    NOM['ou'] = OU

    @_(r'\d+\.\d+')
    def NOMBRE_FLOTTANT(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def NOMBRE(self, t):
        t.value = int(t.value)
        return t

    @_(r"\".*?\"")
    def CHAINE(self, t):
        t.value = self.remove_quotes(str(t.value))
        return t

    @_(r'\#.*')
    def COMMENTAIRE(self, t):
        pass

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def remove_quotes(self, string):
        if string[0] == '\"' or string[0] == '\'':
            return string[1:-1]
        return string

    def error(self, t):
        print("Caractère non autorisé : '%s'" % t.value[0])
        self.index += 1
