// ===== 08072378 FUN_08072378

undefined4 FUN_08072378(int param_1,int *param_2)

{
  uint uVar1;
  int iVar2;
  int iVar3;
  uint uVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  int iVar8;
  undefined4 in_lr;
  
  fast_clear_memory(param_2,0x30);
  iVar2 = DAT_080723f0;
  iVar7 = DAT_080723e8;
  iVar6 = 0;
  if ((*(byte *)(DAT_080723ec * param_1 + DAT_080723e8 + 0x1b) & 0x7f) != 0) {
    iVar8 = 0;
    iVar3 = DAT_080723ec;
    do {
      uVar4 = *(uint *)((*(ushort *)(iVar8 + iVar3 * param_1 + iVar7 + 0x24) & 0x7fff) * 4 + iVar2);
      iVar5 = ((uVar4 & 0x3ffff) >> 9) * 10;
      iVar3 = (DAT_080723f4 & uVar4) * 10;
      uVar1 = (uVar4 & 0x1f00000) >> 0x14;
      if (uVar1 == 0x15) {
        param_2[5] = param_2[5] + 1;
      }
      else if (uVar1 == 0x16) {
        param_2[4] = param_2[4] + 1;
      }
      else {
        uVar1 = (uVar4 & 0x1e000000) >> 0x19;
        if (uVar1 < 5) {
          if (param_2[6] < iVar5) {
            param_2[6] = iVar5;
          }
          if (param_2[7] < iVar3) {
            param_2[7] = iVar3;
          }
          *param_2 = *param_2 + 1;
          if (iVar5 - DAT_08072440 != 0 && DAT_08072440 <= iVar5) {
            param_2[1] = param_2[1] + 1;
          }
        }
        else if (uVar1 < 7) {
          param_2[2] = param_2[2] + 1;
        }
        else {
          param_2[3] = param_2[3] + 1;
        }
        if (param_2[8] < iVar5) {
          param_2[8] = iVar5;
        }
        if (param_2[9] < iVar3) {
          param_2[9] = iVar3;
        }
        param_2[10] = param_2[10] + iVar5;
        param_2[0xb] = param_2[0xb] + iVar3;
      }
      iVar8 = iVar8 + 0x50;
      iVar6 = iVar6 + 1;
      iVar3 = DAT_080724ac;
    } while (iVar6 < (int)(*(byte *)(DAT_080724ac * param_1 + iVar7 + 0x1b) & 0x7f));
  }
  iVar7 = *param_2 + param_2[2] + param_2[3];
  if (0 < iVar7) {
    iVar2 = fast_division(param_2[10],iVar7);
    param_2[10] = iVar2;
    iVar7 = fast_division(param_2[0xb],iVar7);
    param_2[0xb] = iVar7;
  }
  return in_lr;
}


// ===== 08003B5C FUN_08003b5c

undefined4 FUN_08003b5c(uint param_1,undefined2 param_2,uint param_3,uint param_4)

{
  uint *puVar1;
  uint *puVar2;
  undefined4 in_lr;
  
  FUN_08002628();
  puVar1 = DAT_08003bc8;
  *DAT_08003bc8 = *DAT_08003bc8 & DAT_08003bd0 | (DAT_08003bcc & param_1 & 0xffff) << 3;
  puVar2 = (uint *)((param_1 & 0xffff) * 4 + DAT_08003bd4);
  puVar1[3] = ((*puVar2 & 0x3ffff) >> 9) * 10;
  puVar1[4] = (*puVar2 & DAT_08003bd8) * 10;
  *(undefined2 *)((int)puVar1 + 6) = param_2;
  puVar1[9] = param_3;
  puVar1[10] = param_4;
  *(byte *)puVar1 = (byte)*puVar1 & 0xfd;
  return in_lr;
}


