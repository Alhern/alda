#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sly import Parser
from alda.alda_lexer import AldaLexer


class AldaParser(Parser):
    # debugfile = 'parser.out'

    tokens = AldaLexer.tokens

    precedence = (
        ('left', OU),
        ('left', ET),
        ('left', EGAL, NEGAL),
        ('left', PGR, MGR, PEGR, MEGR),
        ('left', PLUS, MOINS),
        ('left', FOIS, DIVISE),
        ('left', MOD),
        ('right', UMOINS),
        ('nonassoc', ALORS),
        ('nonassoc', SINON),
    )

    def __init__(self):
        self.env = {}

    ################################
    #### PLUSIEURS INSTRUCTIONS ####
    ################################

    # Attention : à utiliser uniquement sur la LDC,
    # ces instructions multiples ne fonctionnent pas au sein d'une fonction, condition ou boucle.
    # ECRIS "un" ; ECRIS 2*6 ; test()

    @_('statement')
    def liste_stat(self, p):
        return (p.statement)

    @_('liste_stat PVIRG statement')
    def liste_stat(self, p):
        return ('liste_stat', p.liste_stat, p.statement)

    #######################

    @_('')
    def statement(self, p):
        pass

    @_('var_assigne')
    def statement(self, p):
        return p.var_assigne

    @_('NOM EST expr')
    def var_assigne(self, p):
        return ('var_assigne', p.NOM, p.expr)

    #######################################
    #### INCREMENTATION/DECREMENTATION ####
    #######################################

    # on incrémente de N valeur :
    # a = 0
    # INCR a 1; ECRIS a == 1

    @_('INCR NOM expr')
    def var_assigne(self, p):
        return ('var_assigne', p.NOM, ('plus', ('nom', p.NOM), p.expr))

    # on décrémente de N valeur :
    # a = 1
    # DECR a 1; ECRIS a == 0

    @_('DECR NOM expr')
    def var_assigne(self, p):
        return ('var_assigne', p.NOM, ('moins', ('nom', p.NOM), p.expr))

    ####################
    #### CONDITIONS ####
    ####################

    # SI (1<2) ALORS (ECRIS "INFERIEUR") SINON (ECRIS "SUPERIEUR")

    @_('SI PGAU expr PDRO ALORS PGAU liste_stat PDRO SINON PGAU liste_stat PDRO')
    def statement(self, p):
        return 'si', p.expr, p.liste_stat0, p.liste_stat1

    # a = 1
    # b = 2
    # SI (a < b) ALORS (ECRIS "b est plus grand")

    @_('SI PGAU expr PDRO ALORS PGAU liste_stat PDRO')
    def statement(self, p):
        return 'si', p.expr, p.liste_stat

    ###################
    #### FONCTIONS ####
    ###################

    # Définition de la fonction :
    # FO pinger(): (DE 1 JUSQUA 10 FAIS (ECRIS "ping" ; ECRIS "pong"))

    @_('FO NOM PGAU PDRO DPTS PGAU liste_stat PDRO')
    def statement(self, p):
        return 'fo_def', p.NOM, p.liste_stat

    # Appel de la fonction :
    # pinger()

    @_('NOM PGAU PDRO')
    def statement(self, p):
        return 'fo_appel', p.NOM

    #############################
    #### OPERATEURS LOGIQUES ####
    #############################

    # a = VRAI
    # b = FAUX
    # a OU b
    # = True

    @_('expr OU expr')
    def statement(self, p):
        return 'ou', p.expr0, p.expr1

    # a = VRAI
    # b = FAUX
    # a ET b
    # = False

    @_('expr ET expr')
    def statement(self, p):
        return 'et', p.expr0, p.expr1

    #################
    #### BOUCLES ####
    #################

    # a = 0
    # TANTQUE (a < 25) FAIS (INCR a 1)

    @_('TANTQUE PGAU expr PDRO FAIS PGAU liste_stat PDRO')
    def statement(self, p):
        return 'tantque', p.expr, p.liste_stat

    # DE 1 JUSQUA 10 FAIS (ECRIS "ping" ; ECRIS "pong")

    @_('DE expr JUSQUA expr FAIS PGAU liste_stat PDRO')
    def statement(self, p):
        return 'de', p.expr0, p.expr1, p.liste_stat

    ###############
    #### LISTE ####
    ###############

    # liste = [a, '12', 2*6]

    @_('expr')
    def liste_elem(self, p):
        return p.expr

    @_('liste_elem VIRGULE expr')
    def liste_elem(self, p):
        return 'liste_elem', p.liste_elem, p.expr

    @_('CGAU liste_elem CDRO')
    def expr(self, p):
        return 'liste', p.liste_elem

    #######################

    @_('expr')
    def statement(self, p):
        return p.expr

    @_('ECRIS expr')
    def statement(self, p):
        return 'ecris', p.expr

    ##################
    #### BOOLEENS ####
    ##################

    @_('VRAI')
    def expr(self, p):
        return True

    @_('FAUX')
    def expr(self, p):
        return False

    ######################
    #### ARITHMETIQUE ####
    ######################

    @_('expr PLUS expr')
    def expr(self, p):
        return 'plus', p.expr0, p.expr1

    @_('expr MOINS expr')
    def expr(self, p):
        return 'moins', p.expr0, p.expr1

    @_('expr FOIS expr')
    def expr(self, p):
        return 'fois', p.expr0, p.expr1

    @_('expr DIVISE expr')
    def expr(self, p):
        return 'divise', p.expr0, p.expr1

    @_('expr MOD expr')
    def expr(self, p):
        return 'mod', p.expr0, p.expr1

    @_('MOINS expr %prec UMOINS')
    def expr(self, p):
        return 'moins', ('nombre', 0), p.expr

    ###################################
    #### OPERATEURS DE COMPARAISON ####
    ###################################

    # a == b

    @_('expr EGAL expr')
    def expr(self, p):
        return 'egal', p.expr0, p.expr1

    # a != b

    @_('expr NEGAL expr')
    def expr(self, p):
        return 'negal', p.expr0, p.expr1

    # a > b

    @_('expr PGR expr')
    def expr(self, p):
        return 'pgr', p.expr0, p.expr1

    # a < b

    @_('expr MGR expr')
    def expr(self, p):
        return 'mgr', p.expr0, p.expr1

    # a >= b
    @_('expr PEGR expr')
    def expr(self, p):
        return 'pegr', p.expr0, p.expr1

    # a <= b
    @_('expr MEGR expr')
    def expr(self, p):
        return 'megr', p.expr0, p.expr1

    #######################

    # (2 + 2) * 4

    @_('PGAU expr PDRO')
    def expr(self, p):
        return p.expr

    @_('NOM')
    def expr(self, p):
        return 'nom', p.NOM

    @_('CHAINE')
    def expr(self, p):
        return 'chaine', p.CHAINE

    @_('NOMBRE_FLOTTANT')
    def expr(self, p):
        return 'nombre_flottant', p.NOMBRE_FLOTTANT

    @_('NOMBRE')
    def expr(self, p):
        return 'nombre', p.NOMBRE
