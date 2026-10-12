// ===== 0800DB44 FUN_0800db44

undefined4 FUN_0800db44(uint param_1)

{
  uint uVar1;
  uint uVar2;
  
  uVar2 = (uint)*(ushort *)((param_1 & 0xffff) * 2 + DAT_0800db78);
  if (uVar2 != DAT_0800db7c) {
    if ((int)DAT_0800db7c < (int)uVar2) {
      if (uVar2 == DAT_0800dbdc) {
        return 1;
      }
      if ((int)DAT_0800dbdc < (int)uVar2) {
        if (uVar2 == DAT_0800dc08) {
          return 1;
        }
        if ((int)DAT_0800dc08 < (int)uVar2) {
          if (uVar2 == DAT_0800dc20) {
            return 1;
          }
          uVar1 = DAT_0800dc30;
          if ((int)uVar2 <= (int)DAT_0800dc20) {
            uVar1 = DAT_0800dc20 - 0x13;
          }
        }
        else {
          if (uVar2 == DAT_0800dc08 - 0xa3) {
            return 1;
          }
          uVar1 = DAT_0800dc08 - 0x59;
        }
      }
      else {
        if (uVar2 == DAT_0800dbe0) {
          return 1;
        }
        if ((int)DAT_0800dbe0 < (int)uVar2) {
          if (uVar2 == DAT_0800dbf0) {
            return 1;
          }
          uVar1 = DAT_0800dbf0 + 0x3a;
        }
        else {
          if (uVar2 == DAT_0800dbe0 - 0xa4) {
            return 1;
          }
          uVar1 = DAT_0800dbe0 - 0x89;
        }
      }
    }
    else if ((int)(DAT_0800db7c - 0xbe) < (int)uVar2) {
      uVar1 = DAT_0800dbb8;
      if ((int)uVar2 <= DAT_0800dbb0) {
        if (DAT_0800dbb0 + -1 <= (int)uVar2) {
          return 1;
        }
        if (DAT_0800dbb0 + -0x38 < (int)uVar2) {
          return 0;
        }
        if ((int)uVar2 < DAT_0800dbb0 + -0x39) {
          return 0;
        }
        return 1;
      }
    }
    else {
      if ((int)(DAT_0800db7c - 0xbf) <= (int)uVar2) {
        return 1;
      }
      if (uVar2 == DAT_0800db7c - 0x15d) {
        return 1;
      }
      if ((int)(DAT_0800db7c - 0x15d) < (int)uVar2) {
        if (uVar2 == DAT_0800db90) {
          return 1;
        }
        uVar1 = DAT_0800db90 + 0x1f;
      }
      else {
        if (uVar2 == DAT_0800db80) {
          return 1;
        }
        uVar1 = DAT_0800db80 + 6;
      }
    }
    if (uVar2 != uVar1) {
      return 0;
    }
  }
  return 1;
}


// ===== 080236C4 FUN_080236c4

longlong FUN_080236c4(ushort *param_1)

{
  uint uVar1;
  uint uVar2;
  uint in_lr;
  
  if (((*param_1 & 0x1e00) == 0x800) &&
     ((undefined1 *)
      (*(uint *)((*(ushort *)
                   (((*param_1 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                    DAT_0802375c * ((*param_1 & 0x1ff) >> 8) + DAT_08023760 + 0x24) & 0x7fff) * 4 +
                DAT_08023758) & 0x1f00000) != &DAT_01500000)) goto LAB_08023964;
  uVar2 = (uint)*param_1;
  uVar1 = (*(uint *)(((uVar2 & 0x1ff) >> 1 & 0x7f) * 0x50 + DAT_0802375c * ((uVar2 & 0x1ff) >> 8) +
                     DAT_08023760 + 0x30) & 0xfffff) >> 0xc & 0x7f;
  if (uVar1 != 5) {
    if (uVar1 < 6) {
      if (uVar1 != 0) goto LAB_08023964;
    }
    else if (uVar1 != 10) goto LAB_08023964;
  }
  if (0x14 < (*(uint *)((*(ushort *)
                          (((uVar2 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                           DAT_080237c0 * ((uVar2 & 0x1ff) >> 8) + DAT_080237c4 + 0x24) & 0x7fff) *
                        4 + DAT_080237bc) & 0x1f00000) >> 0x14) {
                    /* WARNING: Subroutine does not return */
    FUN_0800e158((uVar2 & 0x1ff) >> 1,0x20);
  }
LAB_08023964:
  return (ulonglong)in_lr << 0x20;
}


// ===== 0802C920 FUN_0802c920

longlong FUN_0802c920(undefined4 param_1,short param_2)

{
  uint in_lr;
  
  if (param_2 != 0xff) {
                    /* WARNING: Subroutine does not return */
    FUN_0800e158(param_2,0x21);
  }
  return (ulonglong)in_lr << 0x20;
}


// ===== 0801A600 FUN_0801a600

undefined4 FUN_0801a600(int param_1,uint param_2,uint param_3)

{
  undefined4 uVar1;
  int iVar2;
  uint uVar3;
  uint uVar4;
  uint uVar5;
  int iVar6;
  undefined4 in_lr;
  char acStack_2c [4];
  uint local_28;
  uint uStack_24;
  
  uVar5 = param_2 & 0xffff;
  uVar4 = param_3 & 0xffff;
  iVar2 = (param_3 & 0x7f) * 0x50 + DAT_0801a744 * ((param_3 & 0x80) >> 7) + DAT_0801a740;
  local_28 = *(ushort *)(iVar2 + 0x24) & 0x7fff;
  iVar6 = (param_2 & 0x7f) * 0x50 + DAT_0801a744 * ((param_2 & 0x80) >> 7) + DAT_0801a740;
  uStack_24 = *(ushort *)(iVar6 + 0x24) & 0x7fff;
  uVar1 = 3;
  if (param_1 != 0) {
    uVar1 = DAT_0801a748;
  }
  drawing_FUN_08022084(uVar1,uVar5);
  uVar1 = 0x48;
  if (param_1 != 0) {
    uVar1 = DAT_0801a74c;
  }
  drawing_FUN_08022034(uVar1,uVar5,uVar4);
  uVar1 = 3;
  if (param_1 != 0) {
    uVar1 = DAT_0801a748;
  }
  drawing_FUN_08022084(uVar1,uVar4);
  if ((((*(uint *)((*(ushort *)(iVar2 + 0x24) & 0x7fff) * 4 + DAT_0801a750) & 0x1f00000) >> 0x14 <
        0x15) &&
      ((*(uint *)((*(ushort *)(iVar6 + 0x24) & 0x7fff) * 4 + DAT_0801a750) & 0x1f00000) == 0x1600000
      )) && ((*(uint *)((*(ushort *)(iVar6 + 0x24) & 0x7fff) * 4 + DAT_0801a750) & 0xe0000) ==
             0x60000)) {
    acStack_2c[0] = -1;
    iVar2 = FUN_08010a30(DAT_0801a754,0xff,3,0x20,0x106,0,acStack_2c);
    if ((0 < iVar2) && (acStack_2c[0] != -1)) {
      FUN_0801aaa4(param_1,acStack_2c[0]);
      FUN_0801ad6c((*(uint *)(iVar6 + 0x30) & 0xfffff) >> 0x13,iVar2 * 1000);
    }
  }
  uVar3 = (uint)*(ushort *)(local_28 * 2 + DAT_0801a758);
  if (uVar3 == DAT_0801a75c) {
    uVar1 = 0x57;
    if (param_1 != 0) {
      uVar1 = DAT_0801a7a8;
    }
    drawing_FUN_08022034(uVar1,uVar4,1);
    cleanup_card_actions();
                    /* WARNING: Subroutine does not return */
    send_card_to_graveyard(uVar5,0x41,uVar4);
  }
  if (uVar3 == DAT_0801a760) {
    iVar2 = (param_2 & 0x7f) * 0x50 + DAT_0801a818 * ((param_2 & 0x80) >> 7) + DAT_0801a814;
    uVar4 = (uint)*(ushort *)((*(ushort *)(iVar2 + 0x24) & 0x7fff) * 2 + DAT_0801a758);
    if ((uVar4 == DAT_0801a81c) || (uVar4 == DAT_0801a820)) {
      FUN_080314b4(((*(uint *)(iVar2 + 0x30) & 0xfffff) >> 0x13) << 0x1f |
                   param_3 & 0xff | 0x1e600000,param_3 << 0x10 | uVar5);
    }
    else {
      FUN_080314b4(((*(uint *)((param_3 & 0x7f) * 0x50 + DAT_0801a818 * ((param_3 & 0x80) >> 7) +
                               DAT_0801a814 + 0x30) & 0xfffff) >> 0x13) << 0x1f |
                   param_3 & 0xff | 0x1e600000,param_3 << 0x10 | uVar5);
    }
  }
  if (*(short *)(DAT_0801a898 + 0x300) != 0) {
    return in_lr;
  }
                    /* WARNING: Subroutine does not return */
  FUN_08059478((*(byte *)(DAT_0801a89c + DAT_0801a8a0) & 3) >> 1,0xf,param_3 << 0x10 | uVar5);
}


// ===== 08010C10 FUN_08010c10

void FUN_08010c10(uint param_1,short param_2,short param_3)

{
  uint uVar1;
  
  uVar1 = 6;
  if (param_2 == 0) {
    uVar1 = 7;
  }
  if (param_3 == 0) {
    uVar1 = uVar1 | 8;
  }
  show_confirmation_prompt(0,0xff,(uint)(0x10000 << (param_1 & 0xff)) >> 0x10,1,uVar1,0);
  return;
}


