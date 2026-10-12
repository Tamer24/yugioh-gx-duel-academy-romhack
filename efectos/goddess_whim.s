@ Goddess of Whim (ID 4435): una vez por turno, tira una moneda y la llamas; si acertas el ATK
@ se duplica hasta el fin del turno, si no se reduce a la mitad.
@
@ El fn_04 original abre el menu "Select heads or tails" (modo 0x15) en 0x80 y en 0x7F encola
@ un evento 0x4B tipo 4 que en este ROM nadie atiende (la carta esta recortada y su manejador
@ del resultado no esta). Esta funcion deja al original solo el 0x80 y resuelve ella misma:
@
@   0x7F  el menu ya tiro la moneda y mostro "Correct!" o "Miss!" (0x02022250+0x5656: 1 =
@         acerto, 0 = erro): se avisa el resultado (ask_question) y se pasa a 0x7D
@   0x7D  registra un modificador de ATK en la lista de la ranura con el evento 0x4B
@         (FUN_0801A5BC(lado, ranura, ranura, (nibble << 4) | 4)); lo aplica la rutina de
@         efectos/modificador_atk.s enganchada en el tipo 4 del calculador del motor, y el
@         motor lo borra al terminar el turno.
@         Escribir el ATK a mano no sirve: el motor lo recalcula desde la lista.
@
@ p[10] guarda si acerto. Simbolos: ORIGINAL, ASK_QUESTION, EVENTO_MOD.

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    ldr   r2, =0x020204C6
    ldrb  r2, [r2]
    cmp   r2, #0x7f
    beq   .Lresultado
    cmp   r2, #0x7d
    beq   .Laplicar
    ldr   r3, =ORIGINAL           @ 0x80 (menu de cara o cruz) y el resto: original
    bx    r3

.Lresultado:
    push  {r4, lr}
    adds  r4, r0, #0
    ldrb  r0, [r4, #2]
    movs  r1, #8
    tst   r0, r1
    bne   .Lfin0
    ldr   r1, =0x02022250 + 0x5656
    ldrb  r2, [r1]                @ resultado de la moneda del menu: 1 = acerto ("Correct!"),
    movs  r1, #1                  @ 0 = erro ("Miss!"). El menu ya tira la moneda y la muestra:
    ands  r2, r1                  @ tirar otra aca hacia que el cartel y el efecto no coincidieran
    strb  r2, [r4, #10]
    ldr   r0, =.Lacerto
    cmp   r2, #0
    bne   .Lavisar
    ldr   r0, =.Lerro
.Lavisar:
    ldr   r3, =ASK_QUESTION
    mov   ip, r3
    bl    .Lllamar
    movs  r0, #0x7d
    b     .Lfin

.Laplicar:
    push  {r4, lr}
    adds  r4, r0, #0
    ldrh  r1, [r4]
    lsls  r1, r1, #23
    lsrs  r1, r1, #24             @ id de ranura de esta carta (origen y destino)
    ldrb  r0, [r4]
    movs  r2, #1
    ands  r0, r2                  @ lado
    ldrb  r3, [r4, #10]           @ acerto?
    cmp   r3, #0
    beq   .Lmitad
    movs  r3, #0x14               @ nibble 1 (x2), tipo 4
    b     .Lregistrar
.Lmitad:
    movs  r3, #0x24               @ nibble 2 (mitad), tipo 4
.Lregistrar:
    adds  r2, r1, #0              @ destino = esta carta
    ldr   r4, =EVENTO_MOD
    mov   ip, r4
    bl    .Lllamar
    b     .Lfin0

.Lfin0:
    movs  r0, #0
.Lfin:
    pop   {r4}
    pop   {r1}
    bx    r1

.Lllamar:
    bx    ip

    .align 2
.Lacerto:
    .asciz "You called it right! ATK doubled."
    .align 2
.Lerro:
    .asciz "You called it wrong... ATK halved."
    .align 2
    .pool
