// ===== 080188AC FUN_080188ac

void FUN_080188ac(uint param_1,uint param_2)

{
  byte bVar1;
  ushort uVar2;
  uint uVar3;
  int iVar4;
  uint uVar5;
  undefined4 uVar6;
  uint uVar7;
  uint uVar8;
  int iVar9;
  int iVar10;
  uint uVar11;
  uint uVar12;
  uint uVar13;
  int iVar14;
  code *UNRECOVERED_JUMPTABLE;
  char acStack_3c [4];
  uint local_38;
  uint local_34;
  uint local_30;
  uint local_2c;
  uint local_28;
  uint local_24;
  
  uVar11 = param_1 & 0xff;
  uVar7 = param_2 & 0xffff;
  uVar3 = uVar11 >> 7;
  local_38 = param_1 & 0x7f;
  iVar4 = local_38 * 0x50 + iRam08018950 * uVar3 + iRam0801894c;
  local_34 = *(ushort *)(iVar4 + 0x24) & 0x7fff;
  uVar5 = *(uint *)(iVar4 + 0x30) & 0xfffff;
  local_30 = uVar5 >> 0x13;
  uVar12 = uVar5 >> 0xc & 0x7f;
  local_2c = (*(byte *)(iVar4 + 0x33) & 0x1f) >> 4;
  local_28 = (param_2 & 0x8000) >> 0xf;
  uVar5 = (param_2 & 0x7c00) >> 10;
  uVar13 = (param_2 & 8) >> 3;
  if ((local_38 - 100 & 0xff) < 0x1b) {
    drawing_FUN_08022034(0x38,uVar11,uVar7);
    FUN_08019580();
  }
  if (((uVar5 == 0xc) || (uVar5 == 0xf)) && (iVar4 = FUN_080dd52c(local_34), iVar4 != 0)) {
    uVar5 = 0xb;
    uVar7 = local_28 << 0xf | 0x2c00;
  }
  iVar4 = (param_1 & 0x7f) * 0x50 + 0x2b08 * -((int)((param_1 & 0x80) << 0x18) >> 0x1f) +
          0x2022250;
  uVar8 = (uint)*(ushort *)((*(ushort *)(iVar4 + 0x24) & 0x7fff) * 2 + 0x87a8624);
  if (uVar8 == 5170/*?*/) {
    local_24 = 0;
    if (((int)((uint)*(byte *)(iVar4 + 0x33) * 0x8000000) < 0) && (uVar12 == 5)) {
      local_24 = -(uVar5 ^ 5) >> 0x1f;
    }
    if (((((int)((uint)*(byte *)((param_1 & 0x7f) * 0x50 +
                                 0x2b08 * -((int)((param_1 & 0x80) << 0x18) >> 0x1f) +
                                 0x2022250 + 0x33) * 0x8000000) < 0) && (uVar12 == 5)) &&
        (uVar5 == 5)) && (uVar13 == 0)) {
      local_24 = 1;
    }
    if (local_24 != 0) {
      iVar14 = 0x2b08 * -((int)((param_1 & 0x80) << 0x18) >> 0x1f);
      iVar4 = (param_1 & 0x7f) * 0x50;
      iVar9 = iVar4 + iVar14 + 0x2022250;
      iVar10 = 0;
      if ((*(byte *)(iVar9 + 0x3e) & 0xf) != 0) {
        do {
          uVar2 = *(ushort *)(iVar10 * 2 + iVar4 + iVar14 + 0x2022250 + 0x40);
          if (uVar2 >> 8 == 3) {
            uVar6 = 0x23;
            if (((*(uint *)(iVar9 + 0x30) & 0xfffff) >> 0xc & 0x80) != 0) {
              uVar6 = 0x8023;
            }
            drawing_FUN_08022034(uVar6,uVar2 & 0xff,0);
          }
          iVar10 = iVar10 + 1;
          iVar4 = (param_1 & 0x7f) * 0x50;
          iVar9 = iVar4 + iVar14 + 0x2022250;
        } while (iVar10 < (int)(*(byte *)(iVar9 + 0x3e) & 0xf));
      }
      uVar6 = 0x4e;
      if (((*(uint *)((param_1 & 0x7f) * 0x50 +
                      0x2b08 * -((int)((param_1 & 0x80) << 0x18) >> 0x1f) + 0x2022250 +
                     0x30) & 0xfffff) >> 0xc & 0x80) != 0) {
        uVar6 = 0x804e;
      }
      drawing_FUN_08022084(uVar6,uVar11);
    }
  }
  else if (uVar8 == 6126/*?*/) {
    local_24 = 0;
    if (((int)((uint)*(byte *)(iVar4 + 0x33) * 0x8000000) < 0) && (uVar12 == 0)) {
      local_24 = -uVar5 >> 0x1f;
    }
    if ((((int)((uint)*(byte *)((param_1 & 0x7f) * 0x50 +
                                0x2b08 * -((int)((param_1 & 0x80) << 0x18) >> 0x1f) +
                                0x2022250 + 0x33) * 0x8000000) < 0) && (uVar12 == 0)) &&
       ((uVar5 == 0 && (uVar13 == 0)))) {
      local_24 = 1;
    }
    if (local_24 != 0) {
      iVar14 = 0x2b08 * -((int)((param_1 & 0x80) << 0x18) >> 0x1f);
      iVar4 = (param_1 & 0x7f) * 0x50;
      iVar9 = iVar4 + iVar14 + 0x2022250;
      iVar10 = 0;
      if ((*(byte *)(iVar9 + 0x3e) & 0xf) != 0) {
        do {
          uVar2 = *(ushort *)(iVar10 * 2 + iVar4 + iVar14 + 0x2022250 + 0x40);
          if (uVar2 >> 8 == 3) {
            uVar6 = 0x23;
            if (((*(uint *)(iVar9 + 0x30) & 0xfffff) >> 0xc & 0x80) != 0) {
              uVar6 = 0x8023;
            }
            drawing_FUN_08022034(uVar6,uVar2 & 0xff,0);
          }
          iVar10 = iVar10 + 1;
          iVar4 = (param_1 & 0x7f) * 0x50;
          iVar9 = iVar4 + iVar14 + 0x2022250;
        } while (iVar10 < (int)(*(byte *)(iVar9 + 0x3e) & 0xf));
      }
      uVar6 = 0x4e;
      if (((*(uint *)((param_1 & 0x7f) * 0x50 +
                      0x2b08 * -((int)((param_1 & 0x80) << 0x18) >> 0x1f) + 0x2022250 +
                     0x30) & 0xfffff) >> 0xc & 0x80) != 0) {
        uVar6 = 0x804e;
      }
      drawing_FUN_08022084(uVar6,uVar11);
    }
  }
  drawing_FUN_08022034(0x38,uVar11,uVar7);
  local_24 = 0;
  if (uVar12 == 5) {
    uVar7 = *(uint *)(local_34 * 4 + 0x8f243cc);
    if (((uVar7 & 0x1f00000) == 0x1600000) && ((uVar7 & 0xe0000) == 0x60000)) {
      acStack_3c[0] = -1;
      iVar4 = FUN_08010a30(5734/*?*/,0xff,3,0x20,0x106,0,acStack_3c);
      if ((0 < iVar4) && (acStack_3c[0] != -1)) {
        FUN_0801aaa4(uVar3,acStack_3c[0]);
        FUN_0801abf0(uVar3,iVar4 * 1000);
      }
    }
    uVar3 = (uint)*(ushort *)
                   ((*(ushort *)
                      ((param_1 & 0x7f) * 0x50 +
                       0x2b08 * -((int)((param_1 & 0x80) << 0x18) >> 0x1f) + 0x2022250 +
                      0x24) & 0x7fff) * 2 + 0x87a8624);
    if (uVar3 == 5231/*?*/) {
      iVar4 = show_confirmation_prompt(uVar3,uVar11,1 << (local_30 & 0xff) & 0xffff,0x20,0x106,1);
      if (iVar4 == 0) {
        iVar4 = 0;
        do {
          bVar1 = *(byte *)(iVar4 + local_30 * 0xb + 0x2022250 + 0x5610);
          uVar3 = (uint)bVar1;
          if (((uVar3 != 0xff) && (0x1a < (uVar3 & 0x7f) - 100)) &&
             ((iVar9 = (uVar3 & 0x7f) * 0x50 + (uint)(bVar1 >> 7) * 0x2b08 + 0x2022250,
              (int)((uint)*(byte *)(iVar9 + 0x33) * 0x8000000) < 0 &&
              (*(ushort *)((*(ushort *)(iVar9 + 0x24) & 0x7fff) * 2 + 0x87a8624) == 5242/*?*/)
              ))) {
            send_card_to_graveyard(uVar3,0x4001);
            return;
          }
          iVar4 = iVar4 + 1;
        } while (iVar4 < 5);
      }
    }
    else if ((uVar3 == 6205/*?*/) && (uVar5 != 5)) {
      if (uVar5 < 6) {
        if (uVar5 == 0) goto LAB_08018ec6;
      }
      else if (uVar5 == 10) goto LAB_08018ec6;
      uVar3 = *(uint *)((param_1 & 0x7f) * 0x50 +
                        0x2b08 * -((int)((param_1 & 0x80) << 0x18) >> 0x1f) + 0x2022250 +
                       0x30);
      iVar4 = FUN_080314b4(((uVar3 & 0xfffff) >> 0x13) << 0x1f | uVar11 | 0x1c800000,
                           ((uVar3 & 0xfffff) >> 0xc) << 8 | uVar11 |
                           (((uVar3 & 0xfffff) >> 0xc) << 8 | uVar11) << 0x10);
      if (iVar4 != 0) {
        local_24 = 1;
      }
    }
  }
  else if (uVar12 < 6) {
    if (((uVar12 == 0) &&
        (*(ushort *)
          ((*(ushort *)
             ((param_1 & 0x7f) * 0x50 + 0x2b08 * -((int)((param_1 & 0x80) << 0x18) >> 0x1f) +
              0x2022250 + 0x24) & 0x7fff) * 2 + 0x87a8624) == 6205/*?*/)) && (uVar5 != 5))
    {
      if (uVar5 < 6) {
        if (uVar5 == 0) goto LAB_08018ec6;
      }
      else if (uVar5 == 10) goto LAB_08018ec6;
      uVar3 = *(uint *)((param_1 & 0x7f) * 0x50 +
                        0x2b08 * -((int)((param_1 & 0x80) << 0x18) >> 0x1f) + 0x2022250 +
                       0x30);
      iVar4 = FUN_080314b4(((uVar3 & 0xfffff) >> 0x13) << 0x1f | uVar11 | 0x1c800000,
                           ((uVar3 & 0xfffff) >> 0xc) << 8 | uVar11 |
                           (((uVar3 & 0xfffff) >> 0xc) << 8 | uVar11) << 0x10);
      if (iVar4 != 0) {
        local_24 = 1;
      }
    }
  }
  else if (((uVar12 == 10) && (local_2c != 0)) && (uVar3 = FUN_080111b8(), uVar11 == uVar3)) {
    drawing_FUN_08022084(0x22,0xff);
  }
LAB_08018ec6:
  if (uVar5 < 0x10) {
                    /* WARNING: Could not recover jumptable at 0x08018ed6. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(uVar5 * 4 + 0x8018ee4))();
    return;
  }
                    /* WARNING: Could not recover jumptable at 0x0801958e. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*UNRECOVERED_JUMPTABLE)();
  return;
}


