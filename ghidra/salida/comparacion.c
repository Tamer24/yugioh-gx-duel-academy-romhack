// ===== 0803DFE4 FUN_0803dfe4

undefined8 FUN_0803dfe4(byte *param_1)

{
  byte bVar1;
  byte bVar2;
  int iVar3;
  undefined4 uVar4;
  undefined4 in_lr;
  
  bVar1 = param_1[2];
  if ((bVar1 & 8) == 0) {
    bVar2 = *(byte *)(DAT_0803e010 + DAT_0803e014);
    if (bVar2 == 0x7f) {
      iVar3 = show_confirmation_prompt(DAT_0803e068,0xff,3,1,6,1);
      if (iVar3 != 0) {
        if ((*param_1 & 1) == 0) {
          ask_yes_or_no_question(DAT_0803e09c);
        }
        else if ((*(ushort *)(DAT_0803e06c + DAT_0803e070) & 0x1fff) >> 6 < 4) {
          *(ushort *)(DAT_0803e088 + DAT_0803e08c) = bVar1 & 8;
        }
        else {
          *(undefined2 *)(DAT_0803e074 + DAT_0803e078) = 1;
        }
        uVar4 = 0x7e;
        goto LAB_0803e0ba;
      }
    }
    else if (bVar2 < 0x80) {
      if ((bVar2 == 0x7e) && (*(short *)(DAT_0803e0c4 + DAT_0803e0c8) != 0)) {
        FUN_0801b28c(*param_1 & 1,1);
      }
    }
    else if (bVar2 == 0x80) {
      FUN_0801b28c(*param_1 & 1,2);
      uVar4 = 0x7f;
      goto LAB_0803e0ba;
    }
  }
  uVar4 = 0;
LAB_0803e0ba:
  return CONCAT44(in_lr,uVar4);
}


// ===== 08031824 FUN_08031824

undefined8 FUN_08031824(byte *param_1)

{
  byte bVar1;
  undefined4 uVar2;
  uint uVar3;
  int iVar4;
  int iVar5;
  undefined4 in_lr;
  
  iVar5 = 0;
  while( true ) {
    bVar1 = *(byte *)(iVar5 + (1 - (*param_1 & 1)) * 0xb + DAT_08031884 + DAT_08031888);
    if ((((bVar1 != 0xff) && (uVar3 = bVar1 & 0x7f, 0x1a < uVar3 - 100)) &&
        (iVar4 = uVar3 * 0x50 + (uint)(bVar1 >> 7) * DAT_08031890 + DAT_08031884,
        (int)((uint)*(byte *)(iVar4 + 0x33) * 0x8000000) < 0)) &&
       (*(ushort *)((*(ushort *)(iVar4 + 0x24) & 0x7fff) * 2 + DAT_0803188c) == DAT_08031894))
    break;
    iVar5 = iVar5 + 1;
    if (4 < iVar5) {
      uVar2 = 1;
LAB_080318a0:
      return CONCAT44(in_lr,uVar2);
    }
  }
  uVar2 = 0;
  goto LAB_080318a0;
}


// ===== 0803A1B0 FUN_0803a1b0

longlong FUN_0803a1b0(ushort *param_1)

{
  char cVar1;
  int iVar2;
  uint in_lr;
  
  if ((param_1[1] & 8) == 0) {
    cleanup_card_actions();
    iVar2 = 0;
    do {
      cVar1 = *(char *)(iVar2 + (1 - ((byte)*param_1 & 1)) * 0xb + DAT_0803a208);
      if (cVar1 != -1) {
                    /* WARNING: Subroutine does not return */
        send_card_to_graveyard(cVar1,((byte)*param_1 & 1) << 0xf | 0x41,(*param_1 & 0x1ff) >> 1);
      }
      iVar2 = iVar2 + 1;
    } while (iVar2 < 5);
    process_card_actions();
  }
  return (ulonglong)in_lr << 0x20;
}


// ===== 080295E4 FUN_080295e4

undefined8 FUN_080295e4(uint *param_1,uint param_2)

{
  undefined4 uVar1;
  uint uVar2;
  int iVar3;
  undefined4 in_lr;
  
  if ((*param_1 & DAT_080296a8) == 0x4c00) {
LAB_080296c4:
    uVar1 = 1;
  }
  else {
    iVar3 = (param_2 & 0x7f) * 0x50 + ((param_2 & 0x80) >> 7) * DAT_080296b0 + DAT_080296ac;
    if ((((byte)*param_1 & 1) != (*(uint *)(iVar3 + 0x30) & 0xfffff) >> 0x13) &&
       (((*(uint *)(iVar3 + 0x30) & 0xfffff) >> 0xc & 0x7f) == 0)) {
      uVar2 = (uint)*(ushort *)
                     ((*(ushort *)
                        ((((ushort)*param_1 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                         (((ushort)*param_1 & 0x1ff) >> 8) * DAT_080296b0 + DAT_080296ac + 0x24) &
                      0x7fff) * 2 + DAT_080296b4);
      if (((uVar2 != DAT_080296b8) && (uVar2 != DAT_080296bc)) ||
         ((*(ushort *)((*(ushort *)(iVar3 + 0x24) & 0x7fff) * 2 + DAT_080296b4) != DAT_080296c0 ||
          (-1 < (int)((uint)*(byte *)(iVar3 + 0x33) * 0x8000000))))) goto LAB_080296c4;
    }
    uVar1 = 0;
  }
  return CONCAT44(in_lr,uVar1);
}


// ===== 0803DC04 FUN_0803dc04

longlong FUN_0803dc04(ushort *param_1)

{
  int iVar1;
  uint in_lr;
  
  if (((param_1[1] & 8) == 0) && (iVar1 = FUN_08032470(param_1), iVar1 != 0)) {
    FUN_080184c0((byte)*param_1 & 1,param_1[2],(*param_1 & 0x1ff) >> 1);
  }
  return (ulonglong)in_lr << 0x20;
}


// ===== 08032470 FUN_08032470

undefined8 FUN_08032470(ushort *param_1)

{
  int iVar1;
  undefined4 uVar2;
  int iVar3;
  uint uVar4;
  undefined4 in_lr;
  
  iVar3 = (param_1[2] & 0x7f) * 0x50 + DAT_08032528 * ((int)(param_1[2] & 0x80) >> 7);
  uVar4 = *(uint *)(iVar3 + DAT_08032524 + 0x30) & 0xfffff;
  iVar1 = *(int *)(iVar3 + DAT_08032524 + 0x28);
  if ((((uVar4 >> 0xc & 0x7f) != 0) || (((byte)*param_1 & 1) == uVar4 >> 0x13)) ||
     (-1 < (int)((uint)*(byte *)(iVar3 + DAT_08032524 + 0x33) * 0x8000000))) goto LAB_08032568;
  uVar4 = (uint)*(ushort *)
                 ((*(ushort *)
                    (((*param_1 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                     DAT_08032528 * ((*param_1 & 0x1ff) >> 8) + DAT_08032524 + 0x24) & 0x7fff) * 2 +
                 DAT_0803252c);
  if (uVar4 == DAT_08032530) {
joined_r0x08032560:
    uVar2 = 0;
    if (500 < iVar1) goto LAB_0803256a;
LAB_08032562:
    uVar2 = 1;
  }
  else {
    if ((int)DAT_08032530 < (int)uVar4) {
      if (uVar4 == DAT_08032544) {
        uVar2 = 0;
        if (iVar1 <= DAT_08032548) goto LAB_0803256a;
        goto LAB_08032562;
      }
    }
    else {
      iVar1 = *(int *)(iVar3 + DAT_08032524 + 0x2c);
      if (uVar4 == DAT_08032530 - 1) goto joined_r0x08032560;
    }
LAB_08032568:
    uVar2 = 0;
  }
LAB_0803256a:
  return CONCAT44(in_lr,uVar2);
}


// ===== 0803E400 FUN_0803e400

longlong FUN_0803e400(ushort *param_1)

{
  byte bVar1;
  int iVar2;
  undefined4 uVar3;
  uint in_lr;
  
  if ((param_1[1] & 8) == 0) {
    if ((param_1[4] & 0xf) == 1) {
      bVar1 = *(byte *)((int)param_1 + 9);
      iVar2 = FUN_080616b8(param_1,bVar1);
      if (iVar2 != 0) {
        FUN_0801a5bc((byte)*param_1 & 1,(*param_1 & 0x1ff) >> 1,bVar1,4);
        uVar3 = 3;
        if ((*param_1 & 1) != 0) {
          uVar3 = DAT_0803e454;
        }
        drawing_FUN_08022084(uVar3,bVar1);
      }
    }
  }
  return (ulonglong)in_lr << 0x20;
}


// ===== 0803E458 FUN_0803e458

undefined8 FUN_0803e458(byte *param_1)

{
  int iVar1;
  int iVar2;
  undefined4 uVar3;
  uint uVar4;
  int iVar5;
  undefined4 in_lr;
  
  if (((param_1[2] & 8) == 0) && (*(char *)(DAT_0803e514 + DAT_0803e518) == -0x80)) {
    clear_zone_effects(6,0);
    iVar2 = DAT_0803e520;
    iVar1 = DAT_0803e51c;
    iVar5 = 0;
    uVar4 = (uint)*param_1;
    if ((*(ushort *)(DAT_0803e520 * (1 - (uVar4 & 1)) + DAT_0803e51c + 0x1c) & 0x1fff) >> 6 != 0) {
      do {
        remove_card_from_effect_register
                  (*(undefined1 *)(iVar5 + iVar2 * (1 - (uVar4 & 1)) + iVar1 + DAT_0803e524));
        iVar5 = iVar5 + 1;
        uVar4 = (uint)*param_1;
        if ((int)((*(ushort *)(iVar2 * (1 - (uVar4 & 1)) + iVar1 + 0x1c) & 0x1fff) >> 6) <= iVar5)
        break;
      } while (iVar5 < 5);
    }
    iVar1 = DAT_0803e528;
    init_effect_dialogue(0,iVar5,DAT_0803e528,0);
    *(byte *)(iVar1 + -5) = *(byte *)(iVar1 + -5) & 0x3f;
    *(byte *)(iVar1 + -4) = *(byte *)(iVar1 + -4) & 0xfc;
    *(byte *)(iVar1 + -0x24) = *(byte *)(iVar1 + -0x24) & 0xf0 | 2;
    uVar3 = 10;
  }
  else {
    uVar3 = 0;
  }
  return CONCAT44(in_lr,uVar3);
}


// ===== 0803E3AC FUN_0803e3ac

undefined8 FUN_0803e3ac(byte *param_1)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 in_lr;
  
  if ((param_1[2] & 8) == 0) {
    iVar2 = DAT_0803e3f4 * (1 - (*param_1 & 1)) + DAT_0803e3f0;
    if (((*(byte *)(iVar2 + 0x1c) & 0x3f) != 0 || *(char *)(iVar2 + 0x1b) < '\0') &&
       (iVar2 = FUN_08009094(0x10000), iVar2 == 0)) {
      uVar1 = 0x80;
      goto LAB_0803e3fa;
    }
  }
  uVar1 = 0;
LAB_0803e3fa:
  return CONCAT44(in_lr,uVar1);
}


// ===== 080320BC FUN_080320bc

uint FUN_080320bc(byte *param_1)

{
  int iVar1;
  
  iVar1 = (1 - (*param_1 & 1)) * DAT_080320e8 + DAT_080320e4;
  return -((*(byte *)(iVar1 + 0x1c) & 0x3f) << 1 | (uint)(*(byte *)(iVar1 + 0x1b) >> 7)) >> 0x1f;
}


