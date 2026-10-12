@ Exchange (ID 5218): cada jugador se queda con una carta de la mano del otro.
@
@ Reemplaza fn_04. La original abre el modo 6 del menu (vacio en el ROM) y no mueve nada.
@ Se sigue la secuencia de estados de las cartas originales con seleccion en lista
@ (Painful Choice, Aoi):
@   jugador humano   0x80 candidatas + pregunta -> 0x7F ; 0x7F lista (elegir 1) -> 0x7E ;
@                    0x7E intercambio -> 0x64
@   IA (lado 1)      0x80: elige al azar en la mano del jugador y da otra al azar -> 0x64
@ La carta que se entrega la elige el azar (el rival "elige" una de la mano del jugador).
@
@ Intercambio: se intercambian las 0x50 bytes de las dos ranuras y se invierte el bit de
@ dueno (bit 3 de +0x32). Las listas de mano apuntan a ranuras y no se tocan.
@ Importante: tras ask_question hay que devolver un estado EXPLICITO.
@
@ Simbolos: CANDIDATAS, ASK_QUESTION, DIALOGO, AZAR (direcciones Thumb, bit 0 en 1).

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    push  {r4, r5, r6, r7, lr}
    adds  r4, r0, #0              @ r4 = carta
    ldrb  r0, [r4, #2]
    movs  r1, #8
    tst   r0, r1
    bne   .Lfin0                  @ anulada
    ldr   r0, =0x020204C6
    ldrb  r5, [r0]                @ r5 = estado
    cmp   r5, #0x80
    beq   .Lentrada
    cmp   r5, #0x7f
    beq   .Llista
    cmp   r5, #0x7e
    beq   .Lresolver
    b     .Lfin0

.Lentrada:
    ldrb  r0, [r4]
    movs  r1, #1
    tst   r0, r1
    bne   .Lia                    @ la activa el rival (IA)
    bl    .Lcandidatas            @ humano: candidatas + pregunta
    cmp   r0, #0
    beq   .Lfin0
    ldr   r3, =ASK_QUESTION
    mov   ip, r3
    ldr   r0, =.Lmensaje
    bl    .Lllamar
    movs  r0, #0x7f
    b     .Lfin

.Llista:
    bl    .Lcandidatas
    ldr   r3, =DIALOGO            @ init_effect_dialogue(0, 1, 0x02019F24, 1)
    mov   ip, r3
    movs  r0, #0
    movs  r1, #1
    ldr   r2, =0x02019F24
    movs  r3, #1
    bl    .Lllamar
    ldr   r2, =0x02019F00         @ ajustes de Telescope y del modo 1
    ldrb  r0, [r2, #0x1f]
    movs  r1, #0x3f
    ands  r0, r1
    strb  r0, [r2, #0x1f]
    ldr   r3, =0x02019F20
    ldrb  r0, [r3]
    movs  r1, #3
    bics  r0, r1
    strb  r0, [r3]
    ldrb  r0, [r2]
    movs  r1, #0xf0
    ands  r0, r1
    movs  r1, #2
    orrs  r0, r1
    strb  r0, [r2]
    movs  r0, #0x7e
    b     .Lfin

.Lresolver:                       @ humano: r1 = carta elegida del rival
    ldr   r0, =0x02019F24
    ldr   r0, [r0]
    ldr   r1, =0x0007FFFF
    ands  r0, r1
    lsrs  r6, r0, #11             @ r6 = ranura elegida
    cmp   r6, #0xff
    beq   .Lhecho
    movs  r0, #0                  @ mi lado = jugador (0)
    bl    .Lestructura
    adds  r7, r0, #0              @ r7 = mi estructura
    bl    .Lcantidad              @ r0 = cartas en mi mano
    cmp   r0, #0
    beq   .Lhecho
    bl    .Lazar                  @ r0 = indice al azar
    ldr   r1, =0x00002824
    adds  r1, r1, r7
    ldrb  r1, [r1, r0]            @ id de la carta que entrego
    adds  r0, r6, #0
    bl    .Lintercambio
    b     .Lhecho

.Lia:                             @ IA: azar en las dos manos
    movs  r0, #0
    bl    .Lestructura
    adds  r6, r0, #0              @ r6 = estructura del jugador
    bl    .Lcantidad
    cmp   r0, #0
    beq   .Lfin0
    movs  r0, #1
    bl    .Lestructura
    adds  r7, r0, #0              @ r7 = estructura de la IA
    bl    .Lcantidad
    cmp   r0, #0
    beq   .Lfin0
    adds  r0, r6, #0              @ id al azar de la mano del jugador
    bl    .Lcantidad
    bl    .Lazar
    ldr   r1, =0x00002824
    adds  r1, r1, r6
    ldrb  r5, [r1, r0]            @ r5 = id elegido del jugador
    adds  r0, r7, #0
    bl    .Lcantidad
    bl    .Lazar
    ldr   r1, =0x00002824
    adds  r1, r1, r7
    ldrb  r1, [r1, r0]            @ id que entrega la IA
    adds  r0, r5, #0
    bl    .Lintercambio

.Lhecho:
    movs  r0, #0x64               @ cierre habitual de las cartas originales
    b     .Lfin
.Lfin0:
    movs  r0, #0
.Lfin:
    pop   {r4, r5, r6, r7}
    pop   {r1}
    bx    r1

@ ---- subrutinas --------------------------------------------------------------------
.Lllamar:
    bx    ip

.Lcandidatas:                     @ FUN_0805AEB0(mi lado, ID de Aoi, 0): registra la mano rival
    push  {lr}
    ldrb  r0, [r4]
    movs  r1, #1
    ands  r0, r1
    ldr   r1, =6440
    movs  r2, #0
    ldr   r3, =CANDIDATAS
    mov   ip, r3
    bl    .Lllamar
    pop   {r1}
    bx    r1

.Lestructura:                     @ r0 = lado -> r0 = 0x02022250 + lado * 0x2B08
    ldr   r1, =0x00002B08
    muls  r0, r1, r0
    ldr   r1, =0x02022250
    adds  r0, r0, r1
    bx    lr

.Lcantidad:                       @ r0 = estructura -> r0 = cartas en la mano
    ldrb  r1, [r0, #0x1c]
    movs  r2, #0x3f
    ands  r1, r2
    lsls  r1, r1, #1
    ldrb  r2, [r0, #0x1b]
    lsrs  r2, r2, #7
    orrs  r1, r2
    adds  r0, r1, #0
    bx    lr

.Lazar:                           @ r0 = n (> 0) -> r0 = numero al azar en [0, n)
    push  {r4, lr}
    adds  r4, r0, #0
    ldr   r3, =AZAR
    mov   ip, r3
    bl    .Lllamar
    movs  r1, #0xff
    ands  r0, r1                  @ 0..255
.Lmod:
    cmp   r0, r4
    blt   .Lmodfin
    subs  r0, r0, r4
    b     .Lmod
.Lmodfin:
    pop   {r4}
    pop   {r1}
    bx    r1

.Lranura:                         @ r0 = id de ranura -> r0 = direccion; usa r1, r2
    movs  r1, #0x7f
    ands  r1, r0
    movs  r2, #0x50
    muls  r1, r2, r1
    lsrs  r0, r0, #7
    ldr   r2, =0x00002B08
    muls  r0, r2, r0
    adds  r0, r0, r1
    ldr   r2, =0x02022250
    adds  r0, r0, r2
    bx    lr

.Lintercambio:                    @ r0 = id A, r1 = id B: intercambia contenido y dueno
    push  {r4, r5, lr}
    adds  r5, r1, #0
    bl    .Lranura
    adds  r4, r0, #0              @ r4 = direccion de A
    adds  r0, r5, #0
    bl    .Lranura
    adds  r1, r0, #0              @ r1 = direccion de B
    adds  r0, r4, #0
    movs  r2, #0
.Lb:
    ldr   r3, [r0, r2]
    ldr   r5, [r1, r2]
    str   r5, [r0, r2]
    str   r3, [r1, r2]
    adds  r2, #4
    cmp   r2, #0x50
    blt   .Lb
    adds  r0, #0x32               @ bit de dueno
    adds  r1, #0x32
    movs  r3, #0x08
    ldrb  r2, [r0]
    eors  r2, r3
    strb  r2, [r0]
    ldrb  r2, [r1]
    eors  r2, r3
    strb  r2, [r1]
    pop   {r4, r5}
    pop   {r1}
    bx    r1

    .align 2
.Lmensaje:
    .asciz "Select card in the list to swap from your opponent's hand."
    .align 2
    .pool
