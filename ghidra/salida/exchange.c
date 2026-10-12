// ===== 08043A08 FUN_08043a08

undefined8 FUN_08043a08(byte *param_1)

{
  byte bVar1;
  undefined4 uVar2;
  undefined4 in_lr;
  
  if ((param_1[2] & 8) == 0) {
    bVar1 = *(byte *)(DAT_08043a2c + DAT_08043a30);
    if (bVar1 == 0x7f) {
      param_1[9] = (byte)*(undefined2 *)(DAT_08043a70 + DAT_08043a74);
      FUN_08026970(1 - (*param_1 & 1),6,0,0);
      uVar2 = 0x7e;
      goto LAB_08043a92;
    }
    if (bVar1 < 0x80) {
      if (bVar1 == 0x7e) {
        param_1[10] = (byte)*(undefined2 *)(DAT_08043a88 + DAT_08043a8c);
        uVar2 = 100;
        goto LAB_08043a92;
      }
    }
    else if (bVar1 == 0x80) {
      FUN_08026970(*param_1 & 1,6,0,0);
      uVar2 = 0x7f;
      goto LAB_08043a92;
    }
  }
  uVar2 = 0;
LAB_08043a92:
  return CONCAT44(in_lr,uVar2);
}


// ===== 0806B408 FUN_0806b408

undefined8 FUN_0806b408(int param_1,uint param_2,undefined4 param_3,undefined2 param_4)

{
  byte bVar1;
  int iVar2;
  undefined4 uVar3;
  byte *pbVar4;
  int iVar5;
  uint uVar6;
  char *pcVar7;
  uint uVar8;
  undefined4 in_lr;
  undefined1 auStack_118 [256];
  
  iVar5 = DAT_0806b46c;
  iVar2 = DAT_0806b438;
  uVar6 = param_2 & 0xff;
  uVar8 = (param_2 & 0xffff) >> 8;
  pbVar4 = (byte *)(DAT_0806b438 + DAT_0806b43c);
  bVar1 = *pbVar4;
  if (bVar1 == 1) {
    if (param_1 == 0) {
      if (uVar6 < 2) {
                    /* WARNING: Subroutine does not return */
        ask_question(DAT_0806b4f8);
      }
      FUN_080e1ff0(auStack_118,DAT_0806b4ec,uVar6);
                    /* WARNING: Subroutine does not return */
      ask_question(auStack_118);
    }
    pcVar7 = (char *)(DAT_0806b4c8 + DAT_0806b4cc);
    if (((*pcVar7 != '\0') &&
        (iVar2 = DAT_0806b4d0 * param_1 + DAT_0806b438,
        (*(byte *)(iVar2 + 0x1c) & 0x3f) != 0 || *(char *)(iVar2 + 0x1b) < '\0')) &&
       (iVar2 = FUN_0807303c(0,uVar8), iVar2 != 0xff)) {
      FUN_08019598(param_1,iVar2,param_4);
      *pcVar7 = *pcVar7 + -1;
      uVar3 = 0;
      goto FUN_0806b5c0;
    }
  }
  else if (bVar1 < 2) {
    if ((bVar1 == 0) && (uVar6 != 0)) {
      *(undefined1 *)(DAT_0806b46c + DAT_0806b470) = 0;
      *(char *)(iVar5 + DAT_0806b474) = (char)param_2;
      *pbVar4 = *pbVar4 + 1;
      uVar3 = 0;
      goto FUN_0806b5c0;
    }
  }
  else if (bVar1 == 2) {
    clear_zone_effects(5,0);
    for (iVar5 = 0;
        iVar5 < (int)((*(byte *)(iVar2 + 0x1c) & 0x3f) << 1 | (uint)(*(byte *)(iVar2 + 0x1b) >> 7));
        iVar5 = iVar5 + 1) {
      if (*(byte *)(iVar5 + iVar2 + DAT_0806b588) != uVar8) {
        remove_card_from_effect_register();
      }
    }
    iVar2 = FUN_0800b858();
    if (iVar2 != 0) {
      iVar2 = FUN_0800b858();
      if (iVar2 < (int)uVar6) {
        uVar6 = FUN_0800b858();
      }
      iVar2 = DAT_0806b58c;
      init_effect_dialogue(0,uVar6,DAT_0806b58c,1);
      *(byte *)(iVar2 + -5) = *(byte *)(iVar2 + -5) & 0x3f;
      *(byte *)(iVar2 + -4) = *(byte *)(iVar2 + -4) & 0xfc;
      *(byte *)(iVar2 + -0x24) = *(byte *)(iVar2 + -0x24) & 0xf0 | 2;
      *(char *)(DAT_0806b590 + DAT_0806b594) = *(char *)(DAT_0806b590 + DAT_0806b594) + '\x01';
      uVar3 = 0;
      goto FUN_0806b5c0;
    }
  }
  else if (bVar1 == 3) {
    cleanup_card_actions();
    if (uVar6 != 0) {
                    /* WARNING: Subroutine does not return */
      send_card_to_graveyard((*(uint *)(DAT_0806b5cc + 0x24) & 0x7ffff) >> 0xb,1,0xff);
    }
    process_card_actions();
  }
  uVar3 = 1;
FUN_0806b5c0:
  return CONCAT44(in_lr,uVar3);
}


