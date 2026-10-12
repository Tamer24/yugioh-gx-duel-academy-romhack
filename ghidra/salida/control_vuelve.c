// ===== 0802F73C FUN_0802f73c

undefined4 FUN_0802f73c(uint param_1,short param_2,int param_3)

{
  ushort uVar1;
  uint uVar2;
  undefined4 uVar3;
  int iVar4;
  uint uVar5;
  uint uVar6;
  int iVar7;
  int iVar8;
  ushort *puVar9;
  int iVar10;
  undefined4 in_lr;
  
  iVar10 = DAT_0802f7a0;
  iVar4 = (param_1 & 0x7f) * 0x50 + DAT_0802f7a4 * ((int)(param_1 & 0x80) >> 7);
  iVar7 = iVar4 + DAT_0802f7a0;
  uVar5 = (uint)*(ushort *)((*(ushort *)(iVar7 + 0x24) & 0x7fff) * 2 + DAT_0802f79c);
  if (uVar5 != DAT_0802f7a8) {
    if ((int)uVar5 <= (int)DAT_0802f7a8) {
      if (uVar5 == DAT_0802f7ac) {
        uVar5 = (uint)*(byte *)(iVar7 + 0x3c);
        if (uVar5 == 0xff) {
          return in_lr;
        }
        uVar2 = *(uint *)((uVar5 & 0x7f) * 0x50 + DAT_0802f874 * ((int)(uVar5 & 0x80) >> 7) +
                          DAT_0802f7a0 + 0x30);
        if (((uVar2 & 0xfffff) >> 0xc & 0x7f) != 0) {
          return in_lr;
        }
        uVar6 = (*(uint *)(iVar7 + 0x30) & 0xfffff) >> 0x13;
        if (param_2 != 0) {
          uVar6 = 1 - uVar6;
        }
        if (uVar6 == (uVar2 & 0xfffff) >> 0x13) {
          return in_lr;
        }
        puVar9 = (ushort *)(uVar6 * 2 + param_3);
        iVar10 = FUN_08011074(uVar6,*puVar9);
        if (iVar10 != -1) {
          uVar1 = FUN_0801a8a4(uVar5,*puVar9);
          *puVar9 = uVar1 | *puVar9;
          return in_lr;
        }
        uVar3 = send_card_to_graveyard
                          (uVar5,((*(uint *)(iVar7 + 0x30) & 0xfffff) >> 0x13) << 0xf | 0x41,
                           param_1 & 0xffff);
        return uVar3;
      }
      if (uVar5 != DAT_0802f7b0) {
        return in_lr;
      }
      iVar8 = 0;
      if ((*(byte *)(iVar7 + 0x3e) & 0xf) == 0) {
        return in_lr;
      }
      do {
        uVar1 = *(ushort *)(iVar4 + iVar10 + 0x40);
        if (uVar1 >> 8 == 3) {
          uVar3 = 0x23;
          if (((*(uint *)(iVar7 + 0x30) & 0xfffff) >> 0xc & 0x80) != 0) {
            uVar3 = DAT_0802f8e8;
          }
          drawing_FUN_08022034(uVar3,uVar1 & 0xff,param_2 == 0);
        }
        iVar4 = iVar4 + 2;
        iVar8 = iVar8 + 1;
      } while (iVar8 < (int)(*(byte *)(iVar7 + 0x3e) & 0xf));
      return in_lr;
    }
    if (uVar5 != DAT_0802f7cc) {
      if ((int)DAT_0802f7cc < (int)uVar5) {
        if (uVar5 != DAT_0802f7dc) {
          return in_lr;
        }
        uVar5 = *(uint *)(iVar7 + 0x30) & 0xfffff;
        if ((uVar5 >> 0xc & 0x7f) != 0) {
          return in_lr;
        }
        if (param_2 == 0) {
          return in_lr;
        }
        uVar3 = send_card_to_graveyard(param_1,(uVar5 >> 0x13) << 0xf | 0x41,param_1 & 0xffff);
        return uVar3;
      }
      if (uVar5 != DAT_0802f7cc - 0xf9) {
        return in_lr;
      }
    }
  }
  iVar10 = DAT_0802f7a0 + (param_1 & 0x7f) * 0x50 + DAT_0802f950 * ((int)(param_1 & 0x80) >> 7);
  uVar5 = *(uint *)(iVar10 + 0x30) & 0xfffff;
  if (((uVar5 >> 0xc & 0x7f) == 0) && (param_2 != 0)) {
    uVar5 = uVar5 >> 0x13;
    puVar9 = (ushort *)(uVar5 * 2 + param_3);
    uVar2 = FUN_080110dc(uVar5,*puVar9);
    if (uVar2 == 0xffffffff) {
      uVar3 = send_card_to_graveyard(param_1,uVar5 << 0xf | 0x41,param_1 & 0xffff);
      return uVar3;
    }
    FUN_080188ac(param_1,uVar5 << 0xf | (uVar2 & 0x3f) << 4 | 0x1400 |
                         ((*(byte *)(iVar10 + 0x33) & 0x1f) >> 4) << 3);
    *puVar9 = (ushort)(1 << (uVar2 + 5 & 0xff)) | *puVar9;
  }
  return in_lr;
}


