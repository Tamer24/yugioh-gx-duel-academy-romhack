// ===== 080BDC9C FUN_080bdc9c

undefined8 FUN_080bdc9c(uint param_1)

{
  int iVar1;
  uint uVar2;
  int iVar3;
  int iVar4;
  int *piVar5;
  int iVar6;
  uint uVar7;
  uint uVar8;
  uint uVar9;
  undefined4 in_lr;
  
  uVar9 = 0;
  uVar8 = 0;
  if ((param_1 & 0xffff) < 0x30) {
    piVar5 = (int *)((param_1 & 0xffff) * 0x10 + DAT_080bdd44);
    iVar4 = 0;
    do {
      iVar1 = DAT_080bdd48;
      iVar3 = iVar4 * 8;
      uVar7 = (uint)*(ushort *)(iVar3 + *piVar5 + 4);
      iVar6 = 0;
      iVar4 = iVar4 + 1;
      if (uVar7 != 0) {
        do {
          uVar2 = get_ordinal_id(*(undefined2 *)(iVar6 * 2 + *(int *)(iVar3 + *piVar5)));
          if ((*(ushort *)(((uVar2 & 0xffff) - 1) * 0xc + iVar1 + 4) >> 3 & 0xff) != 0) {
            uVar8 = uVar8 + 1 & 0xffff;
          }
          iVar6 = iVar6 + 1;
        } while (iVar6 < (int)uVar7);
      }
      uVar9 = uVar9 + uVar7 & 0xffff;
    } while (iVar4 < 5);
    uVar9 = fast_division(uVar8 * 1000,uVar9);
    uVar9 = uVar9 & 0xffff;
  }
  else {
    uVar9 = 0;
  }
  return CONCAT44(in_lr,uVar9);
}


// ===== 080BDD4C FUN_080bdd4c

undefined4 FUN_080bdd4c(ushort param_1)

{
  undefined4 uVar1;
  
  if (param_1 < 0xc) {
    uVar1 = 0;
  }
  else if (param_1 < 0x16) {
    uVar1 = 1;
  }
  else if (param_1 < 0x21) {
    uVar1 = 2;
  }
  else if (param_1 < 0x2f) {
    uVar1 = 3;
  }
  else if (param_1 == 0x2f) {
    uVar1 = 4;
  }
  else {
    uVar1 = 5;
  }
  return uVar1;
}


// ===== 080BDD80 FUN_080bdd80

undefined8 FUN_080bdd80(uint param_1)

{
  int iVar1;
  undefined4 uVar2;
  uint *puVar3;
  undefined4 in_lr;
  undefined8 uVar4;
  
  puVar3 = (uint *)(DAT_080bddac + DAT_080bddb0);
  iVar1 = FUN_080ce7a0(1,6);
  if (*puVar3 < iVar1 - 5U) {
    if ((param_1 & 0xffff) < 0xb) {
                    /* WARNING: Could not recover jumptable at 0x080bdda8. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      uVar4 = (**(code **)((param_1 & 0xffff) * 4 + DAT_080bddb4))();
      return uVar4;
    }
    uVar2 = 0;
  }
  else {
    uVar2 = 1;
  }
  return CONCAT44(in_lr,uVar2);
}


// ===== 080BDE88 FUN_080bde88

undefined4 FUN_080bde88(uint param_1)

{
  uint uVar1;
  code *UNRECOVERED_JUMPTABLE;
  undefined4 uVar2;
  
  if ((*(byte *)(DAT_080bdeb4 + DAT_080bdeb8) & 0x3f) >> 2 < 8) {
    uVar2 = 1;
  }
  else {
    uVar1 = (param_1 & 0xffff) - 0xc;
    if (uVar1 < 10) {
      UNRECOVERED_JUMPTABLE = *(code **)(uVar1 * 4 + DAT_080bdebc);
                    /* WARNING: Could not recover jumptable at 0x080bdeb2. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      uVar2 = (*UNRECOVERED_JUMPTABLE)(UNRECOVERED_JUMPTABLE,DAT_080bdebc,DAT_080bdeb4);
      return uVar2;
    }
    uVar2 = 0;
  }
  return uVar2;
}


// ===== 080BE090 FUN_080be090

longlong FUN_080be090(uint param_1)

{
  uint uVar1;
  uint in_lr;
  longlong lVar2;
  
  uVar1 = (param_1 & 0xffff) - 0x16;
  if (uVar1 < 0xb) {
                    /* WARNING: Could not recover jumptable at 0x080be0a4. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    lVar2 = (**(code **)(uVar1 * 4 + DAT_080be0a8))();
    return lVar2;
  }
  return (ulonglong)in_lr << 0x20;
}


// ===== 080BE144 FUN_080be144

longlong FUN_080be144(uint param_1)

{
  uint uVar1;
  uint in_lr;
  longlong lVar2;
  
  uVar1 = (param_1 & 0xffff) - 0x21;
  if (0xd < uVar1) {
    return (ulonglong)in_lr << 0x20;
  }
                    /* WARNING: Could not recover jumptable at 0x080be15a. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  lVar2 = (**(code **)(uVar1 * 4 + DAT_080be15c))();
  return lVar2;
}


// ===== 080BE260 FUN_080be260

longlong FUN_080be260(undefined2 param_1)

{
  uint uVar1;
  uint in_lr;
  longlong lVar2;
  
  uVar1 = FUN_080bdd4c(param_1);
  if ((uVar1 & 0xffff) < 5) {
                    /* WARNING: Could not recover jumptable at 0x080be27c. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    lVar2 = (**(code **)((uVar1 & 0xffff) * 4 + DAT_080be280))();
    return lVar2;
  }
  return (ulonglong)in_lr << 0x20;
}


// ===== 080BE2F4 FUN_080be2f4

undefined8 FUN_080be2f4(uint param_1)

{
  short sVar1;
  undefined4 uVar2;
  undefined4 in_lr;
  
  sVar1 = FUN_080be260(param_1 & 0xffff);
  if ((sVar1 == 0) || (*(byte *)((param_1 & 0xffff) * 4 + DAT_080be31c + DAT_080be320) >> 1 == 0)) {
    uVar2 = 0;
  }
  else {
    uVar2 = 1;
  }
  return CONCAT44(in_lr,uVar2);
}


// ===== 080BE32C FUN_080be32c

undefined8 FUN_080be32c(uint param_1,int param_2)

{
  undefined2 uVar1;
  int iVar2;
  int iVar3;
  int *piVar4;
  int iVar5;
  uint uVar6;
  uint uVar7;
  uint uVar8;
  undefined4 in_lr;
  
  uVar7 = 0;
  if ((param_1 & 0xffff) < 0x30) {
    piVar4 = (int *)((param_1 & 0xffff) * 0x10 + DAT_080be3a4);
    iVar3 = 0;
    do {
      iVar2 = iVar3 * 8;
      uVar6 = (uint)*(ushort *)(iVar2 + *piVar4 + 4);
      iVar5 = 0;
      iVar3 = iVar3 + 1;
      uVar8 = uVar7;
      if (uVar6 != 0) {
        do {
          uVar1 = get_ordinal_id(*(undefined2 *)(iVar5 * 2 + *(int *)(iVar2 + *piVar4)));
          uVar7 = uVar8 + 1 & 0xffff;
          *(undefined2 *)(uVar8 * 2 + param_2) = uVar1;
          iVar5 = iVar5 + 1;
          uVar8 = uVar7;
        } while (iVar5 < (int)uVar6);
      }
    } while (iVar3 < 5);
  }
  else {
    uVar7 = 0;
  }
  return CONCAT44(in_lr,uVar7);
}


// ===== 080BE3A8 FUN_080be3a8

longlong FUN_080be3a8(undefined4 param_1,uint param_2)

{
  uint in_lr;
  longlong lVar1;
  
  if (param_2 < 6) {
                    /* WARNING: Could not recover jumptable at 0x080be3ba. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    lVar1 = (**(code **)(param_2 * 4 + DAT_080be3bc))();
    return lVar1;
  }
  return (ulonglong)in_lr << 0x20;
}


// ===== 080BDA90 FUN_080bda90

undefined4 FUN_080bda90(void)

{
  byte bVar1;
  ushort uVar2;
  int iVar3;
  int iVar4;
  uint uVar5;
  undefined4 *puVar6;
  uint uVar7;
  int iVar8;
  byte *pbVar9;
  undefined4 in_lr;
  
  iVar8 = 0;
  puVar6 = (undefined4 *)(DAT_080bdad0 + DAT_080bdacc);
  pbVar9 = (byte *)(DAT_080bdacc + DAT_080bdad4);
  do {
    bVar1 = *pbVar9;
    iVar3 = FUN_080be260(iVar8);
    if (iVar3 != 0) {
      uVar2 = FUN_080bdd4c(iVar8);
      if (uVar2 == 3) {
        iVar3 = fast_modulo(*puVar6,7);
        if (iVar3 == 1) goto LAB_080bdafc;
      }
      else {
        if (uVar2 < 4) {
          if (uVar2 == 2) {
LAB_080bdaee:
            iVar3 = fast_modulo(*puVar6,7);
            if (iVar3 != 6) goto LAB_080bdb24;
          }
        }
        else if (uVar2 == 4) goto LAB_080bdaee;
LAB_080bdafc:
        uVar2 = *(ushort *)(iVar8 * 0x10 + DAT_080bdb18 + 0xc);
        if (bVar1 >> 1 < uVar2) {
          bVar1 = *pbVar9 & 1;
        }
        else {
          bVar1 = *pbVar9 & 1 | ((bVar1 >> 1) - (char)uVar2) * '\x02';
        }
        *pbVar9 = bVar1;
      }
    }
LAB_080bdb24:
    iVar3 = DAT_080bdb78;
    pbVar9 = pbVar9 + 4;
    iVar8 = iVar8 + 1;
    if (0x2f < iVar8) {
      puVar6 = (undefined4 *)(DAT_080bdb78 + DAT_080bdb7c);
      iVar8 = fast_modulo(*puVar6,7);
      if (iVar8 == 1) {
        iVar8 = 0;
        pbVar9 = (byte *)(DAT_080bdb80 + iVar3);
        iVar3 = 0;
        do {
          iVar4 = fast_division2(*puVar6,7);
          uVar5 = fast_modulo(iVar4 + 1,*(undefined2 *)(iVar3 + DAT_080bdb84 + 10));
          if ((iVar8 < 0x1a) && (0x16 < iVar8)) {
            uVar7 = iVar8 - 0x16U & 0xffff;
          }
          else {
            uVar7 = 0;
          }
          iVar4 = FUN_080be260(iVar8);
          if ((iVar4 != 0) && ((uVar5 & 0xffff) == uVar7)) {
            uVar5 = (uint)*(ushort *)(iVar3 + DAT_080bdbd4 + 8) + (uint)(*pbVar9 >> 1) & 0xffff;
            if (99 < uVar5) {
              uVar5 = 99;
            }
            *pbVar9 = *pbVar9 & 1 | (byte)(uVar5 << 1);
          }
          pbVar9 = pbVar9 + 4;
          iVar3 = iVar3 + 0x10;
          iVar8 = iVar8 + 1;
        } while (iVar8 < 0x30);
      }
      return in_lr;
    }
  } while( true );
}


// ===== 080D2574 FUN_080d2574

undefined4 FUN_080d2574(uint param_1,uint param_2)

{
  ushort uVar1;
  uint uVar2;
  byte *pbVar3;
  ushort *puVar4;
  ushort *puVar5;
  uint *puVar6;
  int iVar7;
  uint uVar8;
  ushort *puVar9;
  uint local_2c;
  undefined1 *local_28;
  undefined1 *local_24;
  
  local_28 = (undefined1 *)&local_2c;
  local_24 = (undefined1 *)&local_2c;
  param_1 = param_1 & 0xffff;
  local_2c = param_2 & 0xffff;
  uVar2 = (uint)*(ushort *)(param_1 * 0x10 + DAT_080d2660 + 4);
  iVar7 = 0;
  puVar6 = &local_2c;
  if (local_2c != 0) {
    do {
      puVar5 = (ushort *)(local_28 + -(uVar2 * 2 + 3 & 0xfffffffc));
      FUN_080bd89c(param_1,puVar5);
      iVar7 = iVar7 + 1;
      if (uVar2 != 0) {
        puVar9 = (ushort *)(DAT_080d2664 + DAT_080d2668);
        uVar8 = uVar2;
        do {
          pbVar3 = (byte *)((uint)*puVar9 * 4 + DAT_080d2664);
          *pbVar3 = *pbVar3 & 0xc0 | (byte)param_1 & 0x3f;
          puVar4 = (ushort *)((uint)*puVar9 * 4 + DAT_080d2664);
          *puVar4 = (ushort)DAT_080d266c & *puVar4 | (ushort)((*puVar5 & 0xe000) >> 7);
          uVar1 = *puVar9;
          *puVar9 = uVar1 + 1;
          puVar6 = (uint *)((uint)uVar1 * 4 + DAT_080d2664);
          *puVar6 = *puVar6 & DAT_080d2674 | (DAT_080d2670 & *puVar5) << 9;
          puVar5 = puVar5 + 1;
          uVar8 = uVar8 - 1;
        } while (uVar8 != 0);
      }
      puVar6 = (uint *)local_24;
    } while (iVar7 < (int)local_2c);
  }
  local_24 = (undefined1 *)puVar6;
  return *(undefined4 *)(local_24 + 0x28);
}


// ===== 080D7448 FUN_080d7448

void FUN_080d7448(void)

{
  FUN_080e2df4(DAT_080d7560,0x4000,DAT_080d7564);
  return;
}


// ===== 080D7620 FUN_080d7620

void FUN_080d7620(void)

{
  FUN_080e2df4(DAT_080d768c,0x4000,DAT_080d7690);
  return;
}


// ===== 080D77B0 (sin funcion)
// ===== 080D89A8 (sin funcion)
// ===== 080D8B0C (sin funcion)
// ===== 080D8CC4 (sin funcion)
// ===== 080D8D68 (sin funcion)
// ===== 080D8F00 (sin funcion)
// ===== 080D903C (sin funcion)
// ===== 080D8590 (sin funcion)
// ===== 080D90C4 (sin funcion)
