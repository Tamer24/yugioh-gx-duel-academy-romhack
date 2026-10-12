@ Share the Pain (ID 4889): tributas 1 monstruo propio (coste, lo resuelve fn_14) y el rival
@ tambien tributa 1 monstruo suyo.
@
@ El fn_04 original abre el menu de modo 8 ("elegir monstruo a tributar") para el RIVAL. Si el
@ rival es la IA ese menu no elige nada y el monstruo nunca se sacrifica. Esta funcion, cuando
@ la carta la activa el jugador (lado 0), elige ella el monstruo del rival: el de menor ATK
@ (lo que sacrificaria una IA razonable), y lo manda al cementerio como Aoi/Chosen One
@ (FUN_08018518). Si la activa la IA, el rival es el humano y se deja el original (el menu
@ de modo 8 si funciona para el humano: lo usa fn_14 para el coste propio).
@
@ Comprobacion previa: FUN_08010FA4(rival, 0xFF, 3, ranura) devuelve CUANTOS monstruos del
@ rival se pueden tributar. El original abandonaba si era distinto de 0 (invertido: por eso
@ la carta "no hacia nada" aun con monstruos rivales); aqui se exige que sea mayor que 0.
@ Simbolos: ORIGINAL, A_CEMENTERIO.

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    ldr   r2, =0x020204C6
    ldrb  r2, [r2]
    cmp   r2, #0x80
    bne   .Loriginal
    ldrb  r1, [r0]
    movs  r2, #1
    tst   r1, r2
    bne   .Loriginal              @ la activa la IA: el rival es el humano
    push  {r4, r5, r6, r7, lr}
    adds  r4, r0, #0
    ldrb  r0, [r4, #2]
    movs  r1, #8
    tst   r0, r1
    bne   .Lfin                   @ anulada
    ldrh  r5, [r4]
    lsls  r5, r5, #23
    lsrs  r5, r5, #24             @ id de ranura de esta carta
    movs  r0, #1                  @ rival
    movs  r1, #0xff
    movs  r2, #3
    adds  r3, r5, #0
    ldr   r6, =0x08010FA5
    mov   ip, r6
    bl    .Lllamar
    cmp   r0, #0
    beq   .Lfin                   @ el rival no tiene monstruos tributables
    @ monstruo de menor ATK entre las 5 primeras zonas del rival
    ldr   r6, =0x02022250 + 0x5610 + 11
    movs  r7, #0xff               @ r7 = id elegido
    ldr   r3, =0xFFFF             @ r3 = menor ATK visto
    movs  r2, #0                  @ r2 = indice de zona
.Lbucle:
    ldrb  r0, [r6, r2]
    cmp   r0, #0xff
    beq   .Lsig
    movs  r1, #0x7f
    ands  r1, r0
    movs  r4, #0x50
    muls  r1, r4, r1
    lsrs  r4, r0, #7
    push  {r0}
    ldr   r0, =0x00002B08
    muls  r4, r0, r4
    pop   {r0}
    adds  r1, r1, r4
    ldr   r4, =0x02022250
    adds  r1, r1, r4
    ldrh  r1, [r1, #0x28]         @ ATK
    cmp   r1, r3
    bhi   .Lsig                   @ no es menor
    adds  r3, r1, #0
    adds  r7, r0, #0
.Lsig:
    adds  r2, #1
    cmp   r2, #5
    blt   .Lbucle
    cmp   r7, #0xff
    beq   .Lfin
    movs  r0, #0                  @ lado que activa
    adds  r1, r7, #0              @ id del monstruo del rival
    adds  r2, r5, #0              @ esta carta
    ldr   r6, =A_CEMENTERIO
    mov   ip, r6
    bl    .Lllamar
.Lfin:
    movs  r0, #0
    pop   {r4, r5, r6, r7}
    pop   {r1}
    bx    r1

.Loriginal:
    ldr   r3, =ORIGINAL
    bx    r3
.Lllamar:
    bx    ip
    .align 2
    .pool
