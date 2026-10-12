// ===== 08041F04 FUN_08041f04

longlong FUN_08041f04(byte *param_1)

{
  int iVar1;
  undefined4 uVar2;
  uint uVar3;
  uint in_lr;
  
  if ((param_1[2] & 8) == 0) {
    uVar3 = 0;
    do {
      iVar1 = FUN_0800e874(1 - (*param_1 & 1),uVar3);
      if ((iVar1 != 0) && (iVar1 = FUN_0800e888(1 - (*param_1 & 1),uVar3), iVar1 == 0)) {
        uVar2 = 1;
        if ((*param_1 & 1) != 0) {
          uVar2 = DAT_08041fcc;
        }
        drawing_FUN_08022034(uVar2,1 - (*param_1 & 1),(uVar3 & 0xff) << 8);
        uVar2 = 0x3a;
        if ((*param_1 & 1) == 0) {
          uVar2 = DAT_08041fd0;
        }
        drawing_FUN_08022034(uVar2,uVar3 & 0xffff,0);
        iVar1 = (int)((uint)*param_1 << 0x1f) >> 0x1f;
        uVar2 = FUN_0800e6a0(iVar1 + 1,0,uVar3);
        FUN_0801aa64(-iVar1,uVar2);
        uVar2 = 0x3a;
        if ((*param_1 & 1) == 0) {
          uVar2 = DAT_08041fd0;
        }
        drawing_FUN_08022034(uVar2,uVar3 & 0xffff,0);
      }
      uVar3 = uVar3 + 1;
    } while ((int)uVar3 < 0xb);
  }
  return (ulonglong)in_lr << 0x20;
}


// ===== 08033DA8 FUN_08033da8

void FUN_08033da8(ushort *param_1)

{
  int iVar1;
  int iVar2;
  undefined4 uVar3;
  code *UNRECOVERED_JUMPTABLE;
  
  iVar1 = FUN_08030280((byte)*param_1 & 1,(*param_1 & 0x1ff) >> 1,1000);
  if (iVar1 != 0) {
    iVar1 = 0;
    do {
      iVar2 = FUN_0800e874(1 - ((byte)*param_1 & 1),iVar1);
      if ((iVar2 != 0) && (iVar2 = FUN_0800e888(1 - ((byte)*param_1 & 1),iVar1), iVar2 == 0)) {
        uVar3 = 1;
        goto LAB_08033dfa;
      }
      iVar1 = iVar1 + 1;
    } while (iVar1 < 0xb);
  }
  uVar3 = 0;
LAB_08033dfa:
                    /* WARNING: Could not recover jumptable at 0x08033dfe. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*UNRECOVERED_JUMPTABLE)(uVar3);
  return;
}


// ===== 0802D6EC FUN_0802d6ec

undefined8 FUN_0802d6ec(ushort *param_1)

{
  uint uVar1;
  uint uVar2;
  int iVar3;
  int iVar4;
  undefined4 in_lr;
  
  iVar3 = 0;
  uVar2 = (uint)*(ushort *)
                 ((*(ushort *)
                    (((*param_1 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                     DAT_0802d74c * ((*param_1 & 0x1ff) >> 8) + DAT_0802d748 + 0x24) & 0x7fff) * 2 +
                 DAT_0802d744);
  if (uVar2 == DAT_0802d750) {
LAB_0802d810:
    iVar4 = 2000;
    goto LAB_0802d826;
  }
  if ((int)DAT_0802d750 < (int)uVar2) {
    if (uVar2 == DAT_0802d7ac) goto LAB_0802d800;
    if ((int)DAT_0802d7ac < (int)uVar2) {
      if (DAT_0802d7d8 < (int)uVar2) {
        if (uVar2 != DAT_0802d7f0) {
          uVar1 = DAT_0802d7f0 + 0x56;
          goto FUN_0802d7e8;
        }
      }
      else {
        if (DAT_0802d7d8 + -1 <= (int)uVar2) goto LAB_0802d7fa;
        iVar4 = iVar3;
        if (uVar2 != DAT_0802d7dc) goto LAB_0802d822;
      }
      iVar4 = 500;
    }
    else {
      iVar4 = DAT_0802d80c;
      if (uVar2 != DAT_0802d7ac - 0xfe) {
        if ((int)(DAT_0802d7ac - 0xfe) < (int)uVar2) {
          if (uVar2 != DAT_0802d7c0) {
            iVar4 = iVar3;
            if (uVar2 == DAT_0802d7c0 + 0x83) goto LAB_0802d810;
            goto LAB_0802d822;
          }
        }
        else if (uVar2 != DAT_0802d7ac - 500) {
          uVar1 = DAT_0802d7ac - 0x145;
          goto FUN_0802d7e8;
        }
        goto LAB_0802d800;
      }
    }
  }
  else if (uVar2 == DAT_0802d750 - 0xe9) {
LAB_0802d800:
    iVar4 = 1000;
  }
  else {
    if ((int)(DAT_0802d750 - 0xe9) < (int)uVar2) {
      if (DAT_0802d778 < (int)uVar2) {
        if (uVar2 == DAT_0802d788) {
LAB_0802d7fa:
          iVar4 = 800;
          goto LAB_0802d826;
        }
        uVar1 = DAT_0802d788 + 0x2d;
      }
      else {
        if (DAT_0802d778 + -1 <= (int)uVar2) goto LAB_0802d800;
        uVar1 = DAT_0802d778 - 0x26;
      }
FUN_0802d7e8:
      iVar4 = iVar3;
      if (uVar2 == uVar1) goto LAB_0802d800;
    }
    else {
      iVar4 = DAT_0802d83c;
      if (uVar2 != DAT_0802d754) {
        if ((int)uVar2 <= (int)DAT_0802d754) {
          uVar1 = DAT_0802d754 - 0x12;
          goto FUN_0802d7e8;
        }
        iVar4 = DAT_0802d81c;
        if (uVar2 == 0x11a0) goto LAB_0802d826;
        iVar4 = iVar3;
        if (uVar2 == 0x1295) goto LAB_0802d7fa;
      }
    }
LAB_0802d822:
    if (iVar4 < 1) goto LAB_0802d832;
  }
LAB_0802d826:
  FUN_0801abd0((byte)*param_1 & 1,iVar4);
LAB_0802d832:
  return CONCAT44(in_lr,1);
}


