// ===== 0800E918 FUN_0800e918

undefined4 FUN_0800e918(undefined4 param_1,byte param_2,ushort param_3,uint param_4)

{
  int iVar1;
  int iVar2;
  int iVar3;
  byte *pbVar4;
  undefined4 in_lr;
  
  iVar3 = DAT_0800e9b4;
  iVar1 = DAT_0800e9b0;
  iVar2 = (param_3 & 0x7f) * 0x50 + DAT_0800e9b4 * ((param_3 & 0x80) >> 7) + DAT_0800e9b0;
  *(char *)(iVar2 + 0x3c) = (char)param_4;
  *(byte *)(iVar2 + 0x3d) = param_2;
  iVar2 = (param_4 & 0x7f) * 0x50;
  iVar3 = iVar3 * ((param_4 & 0x80) >> 7);
  pbVar4 = (byte *)(iVar2 + iVar3 + iVar1 + 0x3e);
  if ((*pbVar4 & 0xf) < 0x10) {
    *(ushort *)((*pbVar4 & 0xf) * 2 + iVar2 + iVar3 + iVar1 + 0x40) =
         param_3 & 0xff | (ushort)param_2 << 8;
    *pbVar4 = *pbVar4 & 0xf0 | (*pbVar4 & 0xf) + 1 & 0xf;
  }
  return in_lr;
}


// ===== 0800EAC4 FUN_0800eac4

undefined4 FUN_0800eac4(uint param_1)

{
  byte bVar1;
  int iVar2;
  uint uVar3;
  undefined4 uVar4;
  int iVar5;
  byte *pbVar6;
  int iVar7;
  byte *pbVar8;
  int iVar9;
  uint uVar10;
  undefined4 in_lr;
  
  iVar2 = DAT_0800eb04;
  iVar5 = (param_1 & 0x7f) * 0x50 + DAT_0800eb08 * ((param_1 & 0x80) >> 7) + DAT_0800eb04;
  pbVar8 = (byte *)(iVar5 + 0x3c);
  bVar1 = *pbVar8;
  pbVar6 = (byte *)(iVar5 + 0x3d);
  uVar10 = *pbVar6 & 0xf;
  *pbVar8 = 0xff;
  *pbVar6 = 0;
  iVar5 = 0;
  while( true ) {
    iVar9 = (bVar1 & 0x7f) * 0x50;
    iVar7 = (uint)(bVar1 >> 7) * DAT_0800ec10;
    if ((int)(*(byte *)(iVar9 + iVar7 + iVar2 + 0x3e) & 0xf) <= iVar5) {
      return in_lr;
    }
    if (((uint)*(ushort *)(iVar5 * 2 + iVar9 + iVar7 + iVar2 + 0x40) ==
         (param_1 & 0xff | uVar10 << 8)) && (uVar3 = uVar10 - 1, uVar3 < 0xe)) break;
    iVar5 = iVar5 + 1;
  }
                    /* WARNING: Could not recover jumptable at 0x0800eb34. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  uVar4 = (**(code **)(uVar3 * 4 + DAT_0800eb38))();
  return uVar4;
}


