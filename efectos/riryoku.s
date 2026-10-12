@ Riryoku (ID 5009): elegis 2 monstruos boca arriba; el 1.o pierde la mitad del ATK y el 2.o
@ gana lo perdido, hasta el fin del turno.
@
@ El fn_04 original (formato viejo) leia p[9], p[10] como (lado, zona) y mandaba el evento 0x4B
@ con la cantidad en un campo que hoy es la ranura origen (se truncaba a 8 bits). Ahora registra
@ DOS modificadores de tipo 4 con el evento 0x4B, uno en cada monstruo, con la carta origen =
@ esta carta (Riryoku) y en el nibble alto la posicion del monstruo "mitad" (lado << 3 | zona):
@   FUN_0801A5BC(lado, ranura de Riryoku, destino, (nibble << 4) | 4)
@ efectos/modificador_atk.s hace el calculo: en el monstruo "mitad" el ATK / 2; en el otro,
@ suma el ATK ya reducido del primero.
@
@ Entrada: p[8] & 0xF = 2 elegidos, p[9] = ranura del que pierde, p[10] = ranura del que gana
@ (ids con bit 7 = lado, como los deja fn_18). Simbolos: EVENTO_MOD.

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    push  {r4, r5, r6, r7, lr}
    adds  r4, r0, #0
    ldrb  r0, [r4, #2]
    movs  r1, #8
    tst   r0, r1
    bne   .Lfin                   @ anulada
    ldrb  r0, [r4, #8]
    movs  r1, #0xf
    ands  r0, r1
    cmp   r0, #2
    bne   .Lfin                   @ todavia no estan las dos elecciones
    ldrb  r5, [r4, #9]            @ r5 = el que pierde
    ldrb  r6, [r4, #10]           @ r6 = el que gana
    cmp   r5, r6
    beq   .Lfin
    @ posicion de r5 en la lista de zonas de monstruo de su lado
    lsrs  r2, r5, #7              @ lado
    movs  r3, #11
    muls  r3, r2, r3
    ldr   r0, =0x02022250 + 0x5610
    adds  r3, r3, r0              @ r3 = lista del lado
    movs  r1, #0
.Lbuscar:
    ldrb  r0, [r3, r1]
    cmp   r0, r5
    beq   .Lhallado
    adds  r1, #1
    cmp   r1, #5
    blt   .Lbuscar
    b     .Lfin                   @ no esta en una zona de monstruo
.Lhallado:
    lsls  r2, r2, #3
    orrs  r1, r2                  @ nibble = lado << 3 | zona
    lsls  r1, r1, #4
    movs  r0, #4
    orrs  r1, r0                  @ (nibble << 4) | 4
    adds  r7, r1, #0              @ r7 = tipo del modificador
    @ r4 sigue siendo la carta (p); lado que activa y ranura de Riryoku salen de p
    ldr   r0, =EVENTO_MOD
    mov   ip, r0
    ldrb  r0, [r4]
    movs  r2, #1
    ands  r0, r2                  @ lado que activa
    ldrh  r1, [r4]
    lsls  r1, r1, #23
    lsrs  r1, r1, #24             @ ranura de Riryoku (origen)
    adds  r2, r5, #0              @ destino: el que pierde
    adds  r3, r7, #0
    bl    .Lllamar
    ldr   r0, =EVENTO_MOD
    mov   ip, r0
    ldrb  r0, [r4]
    movs  r2, #1
    ands  r0, r2
    ldrh  r1, [r4]
    lsls  r1, r1, #23
    lsrs  r1, r1, #24
    adds  r2, r6, #0              @ destino: el que gana
    adds  r3, r7, #0
    bl    .Lllamar
.Lfin:
    movs  r0, #0
    pop   {r4, r5, r6, r7}
    pop   {r1}
    bx    r1
.Lllamar:
    bx    ip
    .align 2
    .pool
