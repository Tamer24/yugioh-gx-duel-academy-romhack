@ Chosen One (ID 5101): elegis 1 monstruo y 2 cartas mas de tu mano; el rival saca una al azar.
@
@ La fn_04 original ya trae el final (estados 0x7A..0x78: sorteo, aviso y descarte de las dos
@ no elegidas), pero le falta la seleccion (fn_18). Esta funcion la reemplaza SOLO en los
@ estados 0x80, 0x7F y 0x7E y deja los demas a la original (ORIGINAL).
@
@   humano   0x80 candidatas (mano propia) + pregunta -> 0x7F ; 0x7F lista de 3 -> 0x7E ;
@            0x7E lee las 3 elegidas de 0x02019F24/28/2C, valida (1 monstruo + 2 cartas mas)
@            y las deja en p[9..11] (monstruo primero), p[8] bajo = 3 -> 0x7A
@            Si la eleccion no vale vuelve a 0x80. Cancelar (B) = 0x64, sin efecto.
@   IA       0x80 elige sola el primer monstruo y las dos primeras no-monstruo -> 0x7A
@
@ Candidatas: FUN_0805AEB0(lado del RIVAL, ID de Aoi, 0) registra la mano del lado opuesto,
@ o sea la propia. Resultados de la lista con n = 3: tres u32 consecutivos desde 0x02019F24,
@ cada uno con (v & 0x7FFFF) >> 11 = id de ranura (0xFF = sin elegir). Tipo de la carta en
@ +0x30 (5 bits bajos): < 0x15 monstruo, 0x15/0x16 Magica/Trampa.
@
@ Simbolos: ORIGINAL, CANDIDATAS, ASK_QUESTION, DIALOGO (direcciones Thumb, bit 0 en 1).

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    ldr   r2, =0x020204C6
    ldrb  r2, [r2]
    cmp   r2, #0x79
    beq   .Lpropia                @ 0x79: resolucion propia (ver .Lfinal)
    cmp   r2, #0x7e
    blt   .Loriginal              @ 0x7A: sorteo y aviso originales
.Lpropia:
    push  {r4, r5, r6, r7, lr}
    adds  r4, r0, #0              @ r4 = carta
    ldrb  r0, [r4, #2]
    movs  r1, #8
    tst   r0, r1
    bne   .Lsalir0                @ anulada
    cmp   r2, #0x79
    bne   .Lnofinal
    b     .Lfinal
.Lnofinal:
    cmp   r2, #0x80
    beq   .Lentrada
    cmp   r2, #0x7f
    beq   .Llista
    cmp   r2, #0x7e
    beq   .Lresolver
.Lsalir0:
    b     .Lfin0

.Loriginal:
    ldr   r3, =ORIGINAL
    bx    r3

.Lentrada:
    ldrb  r0, [r4]
    movs  r1, #1
    tst   r0, r1
    bne   .Lia
    bl    .Lcandidatas
    cmp   r0, #0
    beq   .Lsalir0
    ldr   r3, =ASK_QUESTION
    mov   ip, r3
    ldr   r0, =.Lmensaje
    bl    .Lllamar
    movs  r0, #0x7f
    b     .Lfin

.Llista:
    bl    .Lcandidatas
    ldr   r3, =DIALOGO            @ init_effect_dialogue(0, 3, 0x02019F24, 1)
    mov   ip, r3
    movs  r0, #0
    movs  r1, #3
    ldr   r2, =0x02019F24
    movs  r3, #1
    bl    .Lllamar
    ldr   r2, =0x02019F00         @ ajustes de Telescope
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

.Lresolver:
    ldr   r6, =0x02019F24
    movs  r7, #0                  @ r7 = monstruos entre las 3
    movs  r5, #0                  @ r5 = indice
.Lleer:
    lsls  r0, r5, #2
    ldr   r0, [r6, r0]
    ldr   r1, =0x0007FFFF
    ands  r0, r1
    lsrs  r0, r0, #11             @ id de ranura
    cmp   r0, #0xff
    beq   .Lcancelar
    adds  r1, r4, #0
    adds  r1, #9
    strb  r0, [r1, r5]            @ p[9 + i] provisorio
    bl    .Ltipo
    cmp   r0, #0x15
    bge   .Lsigue
    adds  r7, #1
.Lsigue:
    adds  r5, #1
    cmp   r5, #3
    blt   .Lleer
    cmp   r7, #1
    bne   .Lotra_vez              @ no es 1 monstruo + 2 mas: pedir de nuevo
    movs  r5, #0                  @ pone el monstruo en p[9]
.Lbuscar:
    adds  r1, r4, #0
    adds  r1, #9
    ldrb  r0, [r1, r5]
    adds  r6, r0, #0
    bl    .Ltipo
    cmp   r0, #0x15
    blt   .Lencontrado
    adds  r5, #1
    cmp   r5, #3
    blt   .Lbuscar
.Lencontrado:
    adds  r1, r4, #0
    adds  r1, #9
    ldrb  r0, [r1]                @ intercambia p[9] y p[9 + r5]
    ldrb  r2, [r1, r5]
    strb  r2, [r1]
    strb  r0, [r1, r5]
.Lfijar:
    bl    .Lenposiciones          @ p[9..11]: id de ranura -> posicion en la mano
    ldrb  r0, [r4, #8]            @ cuenta de elegidas = 3
    movs  r1, #0xf0
    ands  r0, r1
    adds  r0, #3
    strb  r0, [r4, #8]
    ldr   r0, =0x020204C7         @ sorteo original: tira hasta que salga un indice distinto del
    movs  r1, #0                  @ anterior (0x020204C8) y repite 'contador' veces (0x020204C7).
    strb  r1, [r0]                @ Con anterior = 0 el monstruo (indice 0) no salia nunca: se
    movs  r1, #0xff               @ arranca sin anterior (0xFF) y con un solo tiro
    strb  r1, [r0, #1]
    movs  r0, #0x7a               @ sorteo del rival (original)
    b     .Lfin
.Lotra_vez:
    movs  r0, #0x80
    b     .Lfin
.Lcancelar:
    movs  r0, #0x64
    b     .Lfin

.Lia:                             @ IA: primer monstruo y dos primeras Magicas/Trampas
    ldrb  r0, [r4]
    movs  r1, #1
    ands  r0, r1                  @ mi lado
    bl    .Lestructura
    adds  r6, r0, #0              @ r6 = mi estructura
    bl    .Lcantidad
    adds  r7, r0, #0              @ r7 = cartas en mano
    ldrh  r0, [r4]
    lsls  r0, r0, #23
    lsrs  r0, r0, #24             @ id de esta carta
    mov   ip, r0
    movs  r5, #0                  @ r5 = indice en la mano
    movs  r0, #0xff
    strb  r0, [r4, #9]
    strb  r0, [r4, #10]
    strb  r0, [r4, #11]
.Liabucle:
    cmp   r5, r7
    bge   .Liafin
    ldr   r1, =0x00002824
    adds  r1, r1, r6
    ldrb  r0, [r1, r5]            @ id de la carta de la mano
    mov   r1, ip
    cmp   r0, r1
    beq   .Liasig                 @ no puede elegirse a si misma
    push  {r0}
    bl    .Ltipo
    adds  r2, r0, #0
    pop   {r0}
    cmp   r2, #0x15
    bge   .Liaextra
    ldrb  r1, [r4, #9]
    cmp   r1, #0xff
    bne   .Liasig
    strb  r0, [r4, #9]
    b     .Liasig
.Liaextra:
    ldrb  r1, [r4, #10]
    cmp   r1, #0xff
    bne   .Liaextra2
    strb  r0, [r4, #10]
    b     .Liasig
.Liaextra2:
    ldrb  r1, [r4, #11]
    cmp   r1, #0xff
    bne   .Liasig
    strb  r0, [r4, #11]
.Liasig:
    adds  r5, #1
    b     .Liabucle
.Liafin:
    ldrb  r0, [r4, #9]
    ldrb  r1, [r4, #10]
    ldrb  r2, [r4, #11]
    movs  r3, #0xff
    cmp   r0, r3
    beq   .Lfin0
    cmp   r1, r3
    beq   .Lfin0
    cmp   r2, r3
    beq   .Lfin0
    b     .Lfijar

.Lfinal:                          @ estado 0x79: ya se sorteo la carta; r4 = carta
    ldrb  r0, [r4]
    movs  r1, #1
    ands  r0, r1
    bl    .Lestructura
    adds  r6, r0, #0              @ r6 = mi estructura
    bl    .Lcantidad
    adds  r7, r0, #0              @ r7 = cartas en mano
    movs  r5, #0                  @ posiciones p[9..11] -> ids de ranura (antes de mover nada)
.Lfid:
    adds  r1, r4, #0
    adds  r1, #9
    ldrb  r0, [r1, r5]            @ posicion en la mano
    cmp   r0, r7
    bge   .Lfsal0                @ posicion invalida: no hace nada
    ldr   r2, =0x00002824
    adds  r2, r2, r6
    ldrb  r0, [r2, r0]            @ id de ranura
    strb  r0, [r1, r5]
    adds  r5, #1
    cmp   r5, #3
    blt   .Lfid
    ldr   r0, =0x020204C8
    ldrb  r5, [r0]                @ r5 = indice de la elegida por el rival (0 = el monstruo)
    cmp   r5, #3
    bge   .Lfsal0
    movs  r6, #0                  @ r6 = j
.Lfdesc:
    cmp   r6, r5
    beq   .Lfsig                  @ la elegida se resuelve al final
    adds  r1, r4, #0
    adds  r1, #9
    ldrb  r1, [r1, r6]
    bl    .Lcementerio            @ r1 = id
.Lfsig:
    adds  r6, #1
    cmp   r6, #3
    blt   .Lfdesc
    adds  r1, r4, #0
    adds  r1, #9
    ldrb  r1, [r1, r5]            @ id de la elegida
    cmp   r5, #0
    bne   .Lfmala
    ldrb  r0, [r4]                @ el monstruo: invocacion especial
    movs  r2, #1
    ands  r0, r2
    movs  r2, #1
    movs  r3, #0
    ldr   r6, =INVOCAR
    mov   ip, r6
    bl    .Lllamar
    movs  r0, #0x0a               @ como Monster Reborn tras registrar la invocacion
    b     .Lfin
.Lfmala:
    bl    .Lcementerio
    movs  r0, #0
    b     .Lfin


.Lfsal0:
    b     .Lfin0

.Lcementerio:                     @ r1 = id de ranura -> FUN_08018518(mi lado, id, esta carta)
    push  {lr}
    ldrh  r2, [r4]
    lsls  r2, r2, #23
    lsrs  r2, r2, #24             @ ranura de esta carta
    ldrb  r0, [r4]
    movs  r3, #1
    ands  r0, r3
    ldr   r3, =A_CEMENTERIO
    mov   ip, r3
    bl    .Lllamar
    pop   {r1}
    bx    r1

.Lfin0:
    movs  r0, #0
.Lfin:
    pop   {r4, r5, r6, r7}
    pop   {r1}
    bx    r1

@ ---- subrutinas --------------------------------------------------------------------
.Lenposiciones:                   @ la original (FUN_080195A8) pide la POSICION en la mano
    push  {lr}
    ldrb  r0, [r4]
    movs  r1, #1
    ands  r0, r1
    bl    .Lestructura
    adds  r6, r0, #0              @ r6 = mi estructura
    bl    .Lcantidad
    adds  r7, r0, #0              @ r7 = cartas en mano
    movs  r5, #0                  @ r5 = j (0..2)
.Lpj:
    adds  r1, r4, #0
    adds  r1, #9
    ldrb  r0, [r1, r5]            @ id elegido
    movs  r2, #0                  @ r2 = posicion
.Lpi:
    cmp   r2, r7
    bge   .Lpnext                 @ no esta: se deja el id
    ldr   r3, =0x00002824
    adds  r3, r3, r6
    ldrb  r3, [r3, r2]
    cmp   r3, r0
    beq   .Lpfound
    adds  r2, #1
    b     .Lpi
.Lpfound:
    strb  r2, [r1, r5]
.Lpnext:
    adds  r5, #1
    cmp   r5, #3
    blt   .Lpj
    pop   {r1}
    bx    r1

.Lllamar:
    bx    ip

.Lcandidatas:                     @ registra la mano propia (lado del rival a la funcion)
    push  {lr}
    ldrb  r0, [r4]
    movs  r1, #1
    ands  r0, r1
    eors  r0, r1
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

.Ltipo:                           @ r0 = id de ranura -> r0 = tipo (5 bits de +0x30); usa r1, r2
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
    adds  r0, #0x30
    ldrb  r0, [r0]
    movs  r1, #0x1f
    ands  r0, r1
    bx    lr

    .align 2
.Lmensaje:
    .asciz "Select 1 monster and 2 Spell/Trap Cards in your hand."
    .align 2
    .pool
