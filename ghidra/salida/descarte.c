// ===== 0803CF00 FUN_0803cf00

undefined8 FUN_0803cf00(byte *param_1)

{
  int iVar1;
  undefined4 uVar2;
  undefined4 in_lr;
  
  if ((param_1[2] & 8) == 0) {
    if (*(char *)(DAT_0803cf38 + DAT_0803cf3c) == '\x7f') {
      FUN_08026a3c(*param_1 & 1,2,0,0);
      uVar2 = 0x7e;
      goto LAB_0803cf56;
    }
    if ((*(char *)(DAT_0803cf38 + DAT_0803cf3c) == -0x80) &&
       (iVar1 = FUN_08031824(param_1), iVar1 != 0)) {
      FUN_0801b28c(*param_1 & 1,3);
      uVar2 = 0x7f;
      goto LAB_0803cf56;
    }
  }
  uVar2 = 0;
LAB_0803cf56:
  return CONCAT44(in_lr,uVar2);
}


// ===== 0803D3A8 FUN_0803d3a8

undefined8 FUN_0803d3a8(ushort *param_1)

{
  byte bVar1;
  undefined4 uVar2;
  uint uVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  undefined4 in_lr;
  
  if ((param_1[1] & 8) == 0) {
    if (*(char *)(DAT_0803d3f8 + DAT_0803d3fc) == '}') {
      iVar5 = 0;
      do {
        if (iVar5 == 0) {
          uVar3 = (byte)*param_1 & 1;
        }
        else {
          uVar3 = 1 - ((byte)*param_1 & 1);
        }
        bVar1 = *(byte *)((int)param_1 + uVar3 + 9);
        if (bVar1 != 0) {
          FUN_0801b28c(uVar3,bVar1);
        }
        iVar5 = iVar5 + 1;
      } while (iVar5 < 2);
      uVar2 = 0x7c;
      goto LAB_0803d4d4;
    }
    if (*(char *)(DAT_0803d3f8 + DAT_0803d3fc) == -0x80) {
      cleanup_card_actions();
      iVar5 = 0;
      do {
        if (iVar5 == 0) {
          uVar3 = (byte)*param_1 & 1;
        }
        else {
          uVar3 = 1 - ((byte)*param_1 & 1);
        }
        iVar6 = DAT_0803d490 * uVar3;
        iVar4 = iVar6 + DAT_0803d48c;
        *(byte *)((int)param_1 + uVar3 + 9) =
             (*(byte *)(iVar4 + 0x1c) & 0x3f) << 1 | *(byte *)(iVar4 + 0x1b) >> 7;
        iVar5 = iVar5 + 1;
        if ((*(byte *)(iVar4 + 0x1c) & 0x3f) != 0 || *(char *)(iVar4 + 0x1b) < '\0') {
                    /* WARNING: Subroutine does not return */
          send_card_to_graveyard
                    (*(undefined1 *)(iVar6 + DAT_0803d48c + DAT_0803d494),
                     ((byte)*param_1 & 1) << 0xf | 1,(*param_1 & 0x1ff) >> 1);
        }
      } while (iVar5 < 2);
      process_card_actions();
      uVar2 = 0x7d;
      goto LAB_0803d4d4;
    }
  }
  uVar2 = 0;
LAB_0803d4d4:
  return CONCAT44(in_lr,uVar2);
}


