@ Neo-Spacian Aqua Dolphin (ID 6768, carta nueva): una vez por turno, descartas 1 carta de tu mano;
@ miras la mano del rival y eliges 1 monstruo. Si controlas un monstruo con ATK igual o mayor
@ que el del elegido, lo destruyes y le haces 500 de dano al rival. Si no, recibes 500 de dano.
@
@ Su fila de la tabla de efectos es nueva (receta, "filas_efecto": columnas copiadas de Goddess of
@ Whim, que se activa una vez por turno desde el menu del campo) y esta funcion es su fn_04. Su ID
@ esta en las dos listas del menu del campo (gancho_lista_campo.s y gancho_menu_campo.s).
@
@ Estados (el motor llama a la funcion con 0x020204C6 en 0x80 y a lo que devuelve):
@   0x80  candidatas = mi mano + pregunta                      -> 0x7F
@   0x7F  abre la lista (elegir 1 carta)                       -> 0x7E
@   0x7E  descarta la elegida (coste), quita la bandera 14, registra los monstruos de la mano
@         del rival + pregunta                                  -> 0x7D   (sin monstruos: termina)
@   0x7D  abre la lista (elegir 1 monstruo)                    -> 0x7C
@   0x7C  compara el ATK, destruye y dana (o dana al propio)   -> 0x64
@ La IA (lado 1) no usa el efecto: devuelve 0.
@
@ Moldes: exchange.s (lista y candidatas), spy_mano.s (registrar la mano rival), air_hummingbird.s
@ (una vez por turno). Descartar: FUN_08019598 = A_CEMENTERIO(lado, id, 0xFF).
@ Simbolos del motor: CANDIDATAS, ASK_QUESTION, DIALOGO, CLEAR_ZONE, REGISTRAR, A_CEMENTERIO,
@ DANIO, EVENTO.

    .syntax unified
    .thumb
    .text
    .global _start
_start:
    push  {r4, r5, r6, r7, lr}
    adds  r4, r0, #0              @ r4 = p
    ldrb  r0, [r4, #2]
    movs  r1, #8
    tst   r0, r1
    bne   .Lfin0                  @ anulada
    ldrb  r0, [r4]
    movs  r1, #1
    tst   r0, r1
    bne   .Lfin0                  @ la IA no lo usa
    ldr   r0, =0x020204C6
    ldrb  r5, [r0]                @ r5 = estado
    cmp   r5, #0x80
    beq   .Lentrada
    cmp   r5, #0x7f
    beq   .Llista1
    cmp   r5, #0x7e
    beq   .Ldescarte
    cmp   r5, #0x7d
    beq   .Llista2
    cmp   r5, #0x7c
    beq   .Lresolver
    b     .Lfin0

.Lentrada:
    movs  r0, #0
    bl    .Lestructura
    bl    .Lcantidad
    cmp   r0, #0
    beq   .Lfin0                  @ sin cartas en la mano no hay coste
    bl    .Lcand_mano
    ldr   r0, =.Lm1
    bl    .Lpregunta
    movs  r0, #0x7f
    b     .Lfin

.Llista1:
    bl    .Lcand_mano
    bl    .Ldialogo
    movs  r0, #0x7e
    b     .Lfin

.Ldescarte:
    bl    .Lelegida
    adds  r6, r0, #0
    cmp   r6, #0xff
    beq   .Lhecho                 @ cancelado
    movs  r0, #0                  @ descartar: A_CEMENTERIO(mi lado, id, 0xFF)
    adds  r1, r6, #0
    movs  r2, #0xff
    ldr   r3, =A_CEMENTERIO
    mov   ip, r3
    bl    .Lllamar
    ldrh  r1, [r4]                @ una vez por turno: quita la bandera 14 de esta carta
    lsls  r1, r1, #23
    lsrs  r1, r1, #24
    movs  r0, #0x3c
    movs  r2, #14
    ldr   r3, =EVENTO
    mov   ip, r3
    bl    .Lllamar
    bl    .Lregistrar           @ r0 = monstruos en la mano del rival
    cmp   r0, #0
    beq   .Lhecho
    ldr   r0, =.Lm2
    bl    .Lpregunta
    movs  r0, #0x7d
    b     .Lfin

.Llista2:
    bl    .Lregistrar
    bl    .Ldialogo
    movs  r0, #0x7c
    b     .Lfin

.Lresolver:
    bl    .Lelegida
    adds  r6, r0, #0              @ r6 = ranura del monstruo elegido
    cmp   r6, #0xff
    beq   .Lhecho
    bl    .Lranura
    ldr   r0, [r0, #0x28]         @ ATK del elegido
    bl    .Lmayor                 @ 1 si controlo uno con ATK igual o mayor
    cmp   r0, #0
    beq   .Lpierdo
    ldrh  r2, [r4]                @ causante: esta carta
    lsls  r2, r2, #23
    lsrs  r2, r2, #24
    movs  r0, #1                  @ lado del rival
    adds  r1, r6, #0
    ldr   r3, =A_CEMENTERIO
    mov   ip, r3
    bl    .Lllamar
    movs  r0, #1
    b     .Ldanio
.Lpierdo:
    movs  r0, #0
.Ldanio:
    movs  r1, #0xfa
    lsls  r1, r1, #1              @ 500
    ldr   r3, =DANIO
    mov   ip, r3
    bl    .Lllamar
.Lhecho:
    movs  r0, #0x64
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

.Lcand_mano:                      @ FUN_0805AEB0(lado del RIVAL, ID de Aoi, 0): registra mi mano
    push  {lr}
    movs  r0, #1
    ldr   r1, =6440
    movs  r2, #0
    ldr   r3, =CANDIDATAS
    mov   ip, r3
    bl    .Lllamar
    pop   {r1}
    bx    r1

.Lpregunta:                       @ r0 = texto
    push  {lr}
    ldr   r3, =ASK_QUESTION
    mov   ip, r3
    bl    .Lllamar
    pop   {r1}
    bx    r1

.Ldialogo:                        @ abre la lista con 1 eleccion (ajustes de exchange.s)
    push  {lr}
    ldr   r3, =DIALOGO            @ init_effect_dialogue(0, 1, 0x02019F24, 1)
    mov   ip, r3
    movs  r0, #0
    movs  r1, #1
    ldr   r2, =0x02019F24
    movs  r3, #1
    bl    .Lllamar
    ldr   r2, =0x02019F00
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
    pop   {r1}
    bx    r1

.Lelegida:                        @ -> r0 = id de ranura elegido en la lista (0xFF = ninguno)
    ldr   r0, =0x02019F24
    ldr   r0, [r0]
    ldr   r1, =0x0007FFFF
    ands  r0, r1
    lsrs  r0, r0, #11
    bx    lr

.Lregistrar:                      @ registra los monstruos de la mano del rival -> r0 = cuantos
    push  {r4, r5, r6, r7, lr}
    movs  r0, #6
    movs  r1, #0
    ldr   r3, =CLEAR_ZONE
    mov   ip, r3
    bl    .Lllamar
    movs  r0, #1
    bl    .Lestructura
    adds  r5, r0, #0              @ r5 = estructura del rival
    bl    .Lcantidad
    adds  r6, r0, #0              @ r6 = cartas en su mano
    movs  r7, #0                  @ indice
    movs  r4, #0                  @ cuenta
.Lrb:
    cmp   r7, r6
    bge   .Lrfin
    ldr   r0, =0x00002824
    adds  r0, r0, r5
    ldrb  r0, [r0, r7]            @ id de ranura de la carta
    push  {r0}
    bl    .Lranura
    movs  r1, #0x30
    ldrb  r1, [r0, r1]
    movs  r2, #0x1f
    ands  r1, r2                  @ tipo: menor que 0x15 = monstruo
    cmp   r1, #0x15
    pop   {r0}
    bhs   .Lrn
    ldr   r3, =REGISTRAR
    mov   ip, r3
    bl    .Lllamar
    adds  r4, #1
.Lrn:
    adds  r7, #1
    b     .Lrb
.Lrfin:
    adds  r0, r4, #0
    pop   {r4, r5, r6, r7}
    pop   {r1}
    bx    r1

.Lmayor:                          @ r0 = ATK -> r0 = 1 si controlo un monstruo boca arriba con ATK >= r0
    push  {r4, r5, lr}
    adds  r5, r0, #0
    movs  r4, #0
.Lmz:
    ldr   r0, =0x02022250 + 0x5610
    ldrb  r0, [r0, r4]
    cmp   r0, #0xff
    beq   .Lmn
    bl    .Lranura
    movs  r1, #0x33
    ldrb  r1, [r0, r1]
    movs  r2, #0x10
    tst   r1, r2
    beq   .Lmn                    @ boca abajo
    ldr   r1, [r0, #0x28]
    cmp   r1, r5
    bhs   .Lmsi
.Lmn:
    adds  r4, #1
    cmp   r4, #5
    blt   .Lmz
    movs  r0, #0
    b     .Lmf
.Lmsi:
    movs  r0, #1
.Lmf:
    pop   {r4, r5}
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

    .align 2
.Lm1:
    .asciz "Select 1 card in your hand to discard."
    .align 2
.Lm2:
    .asciz "Select 1 monster in your opponent's hand."
    .align 2
    .pool
