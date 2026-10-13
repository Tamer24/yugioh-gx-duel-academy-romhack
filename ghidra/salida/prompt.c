// ===== 08010A30 FUN_08010a30

undefined8
FUN_08010a30(undefined2 param_1,uint param_2,uint param_3,ushort param_4,undefined2 param_5,
            short param_6,byte *param_7)

{
  byte bVar1;
  short sVar2;
  int iVar3;
  int iVar4;
  uint uVar5;
  int iVar6;
  byte *pbVar7;
  int iVar8;
  ushort uVar9;
  int iVar10;
  undefined4 in_lr;
  uint local_30;
  
  iVar10 = 0;
  if (param_7 != (byte *)0x0) {
    *param_7 = 0xff;
  }
  local_30 = 0;
  while (((int)(param_3 & 0xffff) >> (local_30 & 0xff) & 1U) == 0) {
LAB_08010b9e:
    local_30 = local_30 + 1;
    if (1 < (int)local_30) {
LAB_08010bac:
      return CONCAT44(in_lr,iVar10);
    }
  }
  uVar9 = 1;
  iVar4 = local_30 * 0xb;
  iVar6 = iVar4 + DAT_08010abc;
  iVar3 = DAT_08010ab8 + DAT_08010ac0;
LAB_08010a9e:
  do {
    if ((uVar9 & param_4) != 0) {
      if (uVar9 == 0x20) {
        iVar8 = 5;
        pbVar7 = (byte *)(iVar6 + 5);
        do {
          bVar1 = *pbVar7;
          uVar5 = (uint)bVar1;
          if (((uVar5 != 0xff) && (uVar5 != param_2)) &&
             (sVar2 = FUN_08010724(uVar5,param_1,param_4,param_5), sVar2 != 0)) {
            iVar10 = iVar10 + 1;
            if (param_7 != (byte *)0x0) {
              *param_7 = bVar1;
            }
            if (param_6 != 0) goto LAB_08010b86;
          }
          pbVar7 = pbVar7 + 1;
          iVar8 = iVar8 + 1;
        } while (iVar8 < 10);
      }
      else if (uVar9 < 0x21) {
        if (uVar9 == 1) {
          iVar8 = 0;
          pbVar7 = (byte *)(iVar4 + DAT_08010b10);
          do {
            bVar1 = *pbVar7;
            uVar5 = (uint)bVar1;
            if (((uVar5 != 0xff) && (uVar5 != param_2)) &&
               (sVar2 = FUN_08010724(uVar5,param_1,param_4,param_5), sVar2 != 0)) {
              iVar10 = iVar10 + 1;
              if (param_7 != (byte *)0x0) {
                *param_7 = bVar1;
              }
              if (param_6 != 0) goto LAB_08010b86;
            }
            pbVar7 = pbVar7 + 1;
            iVar8 = iVar8 + 1;
          } while (iVar8 < 5);
        }
      }
      else if (uVar9 == 0x400) {
        bVar1 = *(byte *)(iVar4 + iVar3);
        uVar5 = (uint)bVar1;
        if (((uVar5 != 0xff) && (uVar5 != param_2)) &&
           (sVar2 = FUN_08010724(uVar5,param_1,param_4,param_5), sVar2 != 0)) {
          iVar10 = iVar10 + 1;
          if (param_7 != (byte *)0x0) {
            *param_7 = bVar1;
          }
          if (param_6 != 0) {
LAB_08010b86:
            iVar10 = 1;
            goto LAB_08010bac;
          }
        }
      }
    }
    if (uVar9 != 1) {
      if (uVar9 == 0x20) {
        uVar9 = 0x400;
        goto LAB_08010a9e;
      }
      goto LAB_08010b9e;
    }
    uVar9 = 0x20;
  } while( true );
}


