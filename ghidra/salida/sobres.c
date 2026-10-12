// ===== 080BD72C FUN_080bd72c

undefined4 FUN_080bd72c(int param_1)

{
  undefined2 uVar1;
  short sVar2;
  short sVar3;
  uint uVar4;
  int iVar5;
  uint uVar6;
  uint uVar7;
  undefined4 uVar8;
  int iVar9;
  undefined2 *puVar10;
  uint uVar11;
  ushort *puVar12;
  undefined2 *puVar13;
  uint uVar14;
  undefined4 in_lr;
  
  uVar4 = (uint)*(ushort *)(DAT_080bd7c8 + 0x2f4);
  uVar14 = 0;
  iVar5 = get_card_collection_count(0);
  uVar6 = (uint)*DAT_080bd7cc - iVar5 & 0xffff;
  iVar5 = 0;
  uVar7 = fast_division2(uVar4,3);
  if ((uVar6 != 0) && ((uVar7 & 0xffff) != 0)) {
    do {
      uVar8 = FUN_080e5740();
      sVar2 = fast_modulo2(uVar8,uVar6);
      sVar3 = 0;
      uVar11 = 1;
      iVar5 = iVar5 + 1;
      if (*DAT_080bd7cc != 0) {
        iVar9 = DAT_080bd7d0;
        do {
          if ((*(ushort *)(iVar9 + 4) >> 3 & 0xff) == 0) {
            if (sVar3 == sVar2) {
              sVar2 = FUN_080bd700(uVar11 & 0xffff,param_1,uVar14 & 0xffff);
              if (sVar2 == 0) {
                *(ushort *)(uVar14 * 2 + param_1) = (ushort)uVar11 & (ushort)DAT_080bd7d4;
                uVar14 = uVar14 + 1;
              }
              break;
            }
            sVar3 = sVar3 + 1;
          }
          iVar9 = iVar9 + 0xc;
          uVar11 = uVar11 + 1;
        } while ((int)uVar11 <= (int)(uint)*DAT_080bd894);
      }
    } while ((iVar5 < (int)uVar6) && (iVar5 < (int)(uVar7 & 0xffff)));
  }
  uVar6 = uVar4;
  if ((int)uVar14 < (int)uVar4) {
    puVar12 = (ushort *)(uVar14 * 2 + param_1);
    do {
      uVar8 = FUN_080e5740();
      sVar2 = fast_modulo2(uVar8,*DAT_080bd894);
      sVar3 = FUN_080bd700(sVar2 + 1U,param_1,uVar14 & 0xffff);
      if (sVar3 == 0) {
        *puVar12 = sVar2 + 1U & (ushort)DAT_080bd898;
        puVar12 = puVar12 + 1;
        uVar14 = uVar14 + 1;
      }
    } while ((int)uVar14 < (int)uVar4);
  }
  for (; uVar6 != 0; uVar6 = uVar6 - 1) {
    uVar8 = FUN_080e5740();
    uVar7 = fast_modulo2(uVar8,uVar4);
    uVar8 = FUN_080e5740();
    uVar14 = fast_modulo2(uVar8,uVar4);
    uVar14 = uVar14 & 0xffff;
    puVar13 = (undefined2 *)((uVar7 & 0xffff) * 2 + param_1);
    uVar1 = *puVar13;
    if ((uVar7 & 0xffff) == uVar14) {
      uVar14 = fast_modulo2(uVar14 + 1,uVar4);
      uVar14 = uVar14 & 0xffff;
    }
    puVar10 = (undefined2 *)(uVar14 * 2 + param_1);
    *puVar13 = *puVar10;
    *puVar10 = uVar1;
  }
  return in_lr;
}


// ===== 080BD89C FUN_080bd89c

undefined4 FUN_080bd89c(uint param_1,ushort *param_2)

{
  byte bVar1;
  ushort uVar2;
  byte bVar3;
  ushort *puVar4;
  uint uVar5;
  ushort uVar6;
  short sVar7;
  undefined4 uVar8;
  int iVar9;
  uint uVar10;
  int *piVar11;
  int iVar12;
  uint uVar13;
  uint uVar14;
  int *piVar15;
  byte *pbVar16;
  int iVar17;
  int iVar18;
  ushort *puVar19;
  uint uVar20;
  undefined4 in_lr;
  
  param_1 = param_1 & 0xffff;
  piVar15 = (int *)(param_1 * 0x10 + DAT_080bd8fc);
  uVar8 = FUN_080e5740();
  iVar9 = fast_modulo2(uVar8,DAT_080bd900);
  uVar10 = (uint)*(ushort *)(piVar15 + 1);
  uVar20 = 0;
  pbVar16 = (byte *)(param_1 * 4 + DAT_080bd904 + DAT_080bd908);
  bVar1 = *pbVar16;
  bVar3 = bVar1 >> 1;
  if (bVar3 != 0) {
    *pbVar16 = bVar1 & 1 | (bVar3 - 1) * '\x02';
  }
  if (param_1 == 0x2f) {
    FUN_080bd72c(param_2);
  }
  else {
    iVar18 = 0;
    do {
      piVar11 = (int *)((4U - iVar18) * 8 + *piVar15);
      iVar17 = *piVar11;
      sVar7 = (short)piVar11[1];
      if (((iVar9 < (int)(uint)*(ushort *)(iVar18 * 2 + DAT_080bda80)) && (iVar17 != 0)) &&
         (sVar7 != 0)) {
        uVar8 = FUN_080e5740();
        iVar12 = fast_modulo2(uVar8,sVar7);
        uVar2 = *(ushort *)(iVar12 * 2 + iVar17);
        uVar6 = get_ordinal_id(uVar2);
        if ((uVar6 != 0) && (uVar6 < *DAT_080bda84)) {
          *param_2 = (ushort)((4U - iVar18 & 7) << 0xd) | uVar2 & (ushort)DAT_080bd92c;
          uVar20 = 1;
          break;
        }
      }
      iVar18 = iVar18 + 1;
    } while (iVar18 < 4);
    iVar18 = *(int *)*piVar15;
    iVar9 = ((int *)*piVar15)[1];
    uVar13 = uVar10;
    puVar4 = param_2;
    uVar14 = DAT_080bda88;
    if (uVar20 < uVar10) {
      puVar19 = param_2 + uVar20;
      do {
        uVar8 = FUN_080e5740();
        iVar17 = fast_modulo2(uVar8,(short)iVar9);
        uVar2 = *(ushort *)(iVar17 * 2 + iVar18);
        sVar7 = FUN_080bd700(uVar2,param_2,uVar20 & 0xffff);
        if (((sVar7 == 0) && (uVar6 = get_ordinal_id(uVar2), uVar6 != 0)) && (uVar6 < *DAT_080bda84)
           ) {
          *puVar19 = uVar2 & (ushort)DAT_080bda88;
          puVar19 = puVar19 + 1;
          uVar20 = uVar20 + 1;
        }
        uVar14 = DAT_080bda88;
      } while ((int)uVar20 < (int)uVar10);
    }
    for (; uVar5 = DAT_080bda88, uVar20 = uVar10, uVar13 != 0; uVar13 = uVar13 - 1) {
      uVar2 = *puVar4;
      uVar20 = DAT_080bda88 & uVar2;
      DAT_080bda88 = uVar14;
      uVar6 = get_ordinal_id(uVar20);
      *puVar4 = uVar2 & 0xe000 | uVar6 & (ushort)uVar5;
      puVar4 = puVar4 + 1;
      uVar14 = DAT_080bda88;
      DAT_080bda88 = uVar5;
    }
    for (; DAT_080bda88 = uVar14, uVar20 != 0; uVar20 = uVar20 - 1) {
      uVar8 = FUN_080e5740();
      uVar13 = fast_modulo2(uVar8,uVar10);
      uVar8 = FUN_080e5740();
      uVar14 = fast_modulo2(uVar8,uVar10);
      uVar14 = uVar14 & 0xffff;
      uVar2 = param_2[uVar13 & 0xffff];
      if ((uVar13 & 0xffff) == uVar14) {
        uVar14 = fast_modulo2(uVar14 + 1,uVar10);
        uVar14 = uVar14 & 0xffff;
      }
      param_2[uVar13 & 0xffff] = param_2[uVar14];
      param_2[uVar14] = uVar2;
      uVar14 = DAT_080bda88;
    }
  }
  return in_lr;
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


// ===== 080BDC30 FUN_080bdc30

int FUN_080bdc30(uint param_1)

{
  int iVar1;
  
  if ((param_1 & 0xffff) < 0x30) {
    iVar1 = *(int *)((param_1 & 0xffff) * 0xc + DAT_080bdc50) + DAT_080bdc54;
  }
  else {
    iVar1 = 0;
  }
  return iVar1;
}


// ===== 080BDC58 shop_show_packs

int shop_show_packs(uint param_1,short param_2)

{
  int iVar1;
  
  if ((param_1 & 0xffff) < 0x30) {
    if (param_2 == 0) {
      iVar1 = DAT_080bdc78 + 4;
    }
    else {
      iVar1 = DAT_080bdc90 + 8;
    }
    iVar1 = *(int *)((param_1 & 0xffff) * 0xc + iVar1) + DAT_080bdc94;
  }
  else {
    iVar1 = 0;
  }
  return iVar1;
}


// ===== 080BD550 dialog_update_and_check_busy

undefined8 dialog_update_and_check_busy(void)

{
  int iVar1;
  short sVar2;
  uint uVar3;
  uint *puVar4;
  undefined4 in_lr;
  
  iVar1 = DAT_080bd5bc;
  puVar4 = *(uint **)(DAT_080bd56c + 0x1c8);
  if ((puVar4 == (uint *)0x0) || (puVar4[0x10] == 0)) {
    uVar3 = 1;
  }
  else if (*(int *)((short)puVar4[5] * 4 + DAT_080bd5bc) == 0) {
    *puVar4 = *puVar4 & 0xfffffffe;
    uVar3 = puVar4[1];
  }
  else {
    *puVar4 = *puVar4 | 1;
    sVar2 = call_function_bx_r0(*(undefined4 *)((short)puVar4[5] * 4 + iVar1));
    if (sVar2 != 0) {
      *(byte *)(puVar4 + 0x66) = (byte)puVar4[0x66] & 0xfe;
      *(short *)(puVar4 + 5) = (short)puVar4[5] + 1;
      *(undefined2 *)((int)puVar4 + 0x16) = 0;
    }
    uVar3 = 0;
  }
  return CONCAT44(in_lr,uVar3);
}


