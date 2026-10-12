@ Electromagnetic Bagworm (ID 5040), fn_04: toma el control de la Maquina elegida "until the
@ end of your next turn".
@ La original leia p[9] como (lado) y fijaba la zona en 0 (formato viejo); ahora p[9] es el id
@ de ranura (bit 7 = lado), como en Jowls of Dark Demise / Change of Heart (0x0803EB98):
@ FUN_0801A8A4(id, 0) hace el traspaso.
@ Comprueba: eleccion hecha (p[8] & 0xF = 1), objetivo del rival, tipo Maquina (7) y cara arriba.
@
@ Duracion. Change of Heart marca al monstruo con la bandera 0x15 (evento 0x3B) y la End Phase
@ de ESE turno lo devuelve (FUN_08065BF8). Bagworm dura hasta el fin de MI turno siguiente, asi
@ que en vez de la bandera deja en la lista de modificadores de la Maquina una entrada de tipo 5
@ (tipo sin uso: el calculador de ATK no hace nada con el) con origen = esta carta:
@   FUN_0801A5BC(lado que activa, ranura de esta carta, id objetivo, 5 | saltear << 4)
@ "saltear" = 1 si se activo en mi propio turno (volteo manual): ese fin de turno no cuenta.
@ efectos/gancho_fin_control.s lee esa entrada en la End Phase y devuelve el control.
@
@ Segundo efecto ("the ATK and DEF of the monster that destroyed this card are decreased by 500
@ points"): el motor llama a esta misma funcion con tipo de efecto 4 ((p[1] >> 1) & 0xF) y el
@ monstruo que la destruyo en p[4]; el volteo es el tipo 3. Como Rigorous Reaver (0x08042228),
@ el tipo 4 se delega en la fn_04 de Slate Warrior (0x08042078), que deja en ese monstruo un
@ modificador de tipo 10 (-500 ATK y DEF). Lo dispara efectos/gancho_destruida_batalla_*.s.

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    ldrb  r1, [r0, #1]
    lsls  r1, r1, #27
    lsrs  r1, r1, #28             @ tipo de efecto
    cmp   r1, #4
    bne   .Lvolteo
    ldr   r1, =0x08042079         @ destruida en batalla: como Slate Warrior
    bx    r1
.Lvolteo:
    push  {r4, r5, lr}
    adds  r4, r0, #0
    ldrb  r0, [r4, #2]
    movs  r1, #8
    tst   r0, r1
    bne   .Lfin                   @ anulada
    ldrb  r0, [r4, #8]
    movs  r1, #0xf
    ands  r0, r1
    cmp   r0, #1
    bne   .Lfin
    ldrb  r5, [r4, #9]            @ id del objetivo
    lsrs  r0, r5, #7
    ldrb  r1, [r4]
    movs  r2, #1
    ands  r1, r2
    cmp   r0, r1
    beq   .Lfin                   @ tiene que ser del rival
    @ direccion de la ranura objetivo
    movs  r0, #0x7f
    ands  r0, r5
    movs  r1, #0x50
    muls  r0, r1, r0
    lsrs  r2, r5, #7
    ldr   r1, =0x00002B08
    muls  r1, r2, r1
    adds  r0, r0, r1
    ldr   r1, =0x02022250
    adds  r2, r0, r1              @ r2 = ranura
    adds  r0, r2, #0
    adds  r0, #0x33
    ldrb  r0, [r0]
    movs  r1, #0x30
    ands  r0, r1
    cmp   r0, #0x20
    beq   .Lfin                   @ boca abajo
    ldrh  r0, [r2, #0x24]
    lsls  r0, r0, #17
    lsrs  r0, r0, #15             @ indice * 4
    ldr   r1, =0x08F243CC         @ tabla de stats
    ldr   r0, [r0, r1]
    ldr   r1, =0x01F00000
    ands  r0, r1
    lsrs  r0, r0, #20
    cmp   r0, #7                  @ tipo Maquina
    bne   .Lfin
    @ se puede controlar? (FUN_0801A8A4(id, 0) distinto de 0, como Jowls)
    ldr   r3, =0x0801A8A5
    adds  r0, r5, #0
    movs  r1, #0
    bl    .Lllamar
    cmp   r0, #0
    beq   .Lfin
    ldr   r0, =EVENTO_MOD
    mov   ip, r0
    ldrb  r0, [r4]
    movs  r2, #1
    ands  r0, r2                  @ lado que activa
    ldrh  r1, [r4]
    lsls  r1, r1, #23
    lsrs  r1, r1, #24             @ ranura de esta carta
    adds  r2, r5, #0
    ldr   r3, =0x0202787E         @ J0 + 0x562E: bit 1 = jugador del turno
    ldrb  r3, [r3]
    lsrs  r3, r3, #1
    eors  r3, r0                  @ bit 0 = 0 si es mi turno
    mvns  r3, r3
    lsls  r3, r3, #31
    lsrs  r3, r3, #27             @ 0x10 si es mi turno (saltear ese fin de turno)
    adds  r3, #5                  @ tipo 5
    bl    .Lllamar_ip
.Lfin:
    movs  r0, #0
    pop   {r4, r5}
    pop   {r1}
    bx    r1
.Lllamar:
    bx    r3
.Lllamar_ip:
    bx    ip
    .align 2
    .pool
