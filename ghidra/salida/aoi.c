// ===== 0803F4A0 FUN_0803f4a0

undefined8 FUN_0803f4a0(ushort *param_1)

{
  byte bVar1;
  uint uVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  undefined4 uVar7;
  uint uVar8;
  uint uVar9;
  undefined4 in_lr;
  
  iVar4 = DAT_0803f570;
  iVar3 = DAT_0803f56c;
  iVar6 = DAT_0803f568;
  if ((param_1[1] & 8) == 0) {
    bVar1 = *(byte *)(DAT_0803f4d0 + DAT_0803f4d4);
    if (bVar1 == 0x7e) {
      drawing_FUN_08022084(2,(*(uint *)(DAT_0803f634 + 0x24) & 0x7ffff) >> 0xb);
      uVar7 = 0x7d;
      goto LAB_0803f6e0;
    }
    if (bVar1 < 0x7f) {
      if (bVar1 == 0x7d) {
        uVar9 = (uint)*param_1;
        uVar8 = (uint)*(ushort *)
                       ((*(ushort *)
                          (((uVar9 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                           DAT_0803f684 * ((uVar9 & 0x1ff) >> 8) + DAT_0803f680 + 0x24) & 0x7fff) *
                        2 + DAT_0803f67c);
        if (uVar8 == DAT_0803f688) {
          FUN_0801859c((byte)*param_1 & 1,(*(uint *)(DAT_0803f6ec + 0x24) & 0x7ffff) >> 0xb,1,
                       (uVar9 & 0x1ff) >> 1);
          uVar7 = 0x24;
          if ((*param_1 & 1) == 0) {
            uVar7 = DAT_0803f6f0;
          }
          drawing_FUN_080220d4(uVar7);
        }
        else {
          uVar2 = DAT_0803f6ac;
          if ((int)uVar8 <= (int)DAT_0803f688) {
            uVar2 = DAT_0803f688 - 7;
          }
          if (uVar8 == uVar2) {
            FUN_08018518((byte)*param_1 & 1,(*(uint *)(DAT_0803f6b0 + 0x24) & 0x7ffff) >> 0xb,
                         (uVar9 & 0x1ff) >> 1);
          }
        }
      }
    }
    else {
      if (bVar1 == 0x7f) {
        fusion_summon_dialogue
                  ((byte)*param_1 & 1,0x12,
                   *(undefined2 *)
                    ((*(ushort *)
                       (((*param_1 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                        DAT_0803f61c * ((*param_1 & 0x1ff) >> 8) + DAT_0803f618 + 0x24) & 0x7fff) *
                     2 + DAT_0803f614),0);
        uVar7 = 0x7e;
        goto LAB_0803f6e0;
      }
      if ((bVar1 == 0x80) &&
         (iVar5 = FUN_0805aeb0((byte)*param_1 & 1,
                               *(undefined2 *)
                                ((*(ushort *)
                                   (((*param_1 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                                    DAT_0803f570 * ((*param_1 & 0x1ff) >> 8) + DAT_0803f56c + 0x24)
                                 & 0x7fff) * 2 + DAT_0803f568),0), iVar5 != 0)) {
        if ((*param_1 & 1) == 0) {
          uVar8 = (uint)*(ushort *)
                         ((*(ushort *)
                            (((*param_1 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                             iVar4 * ((*param_1 & 0x1ff) >> 8) + iVar3 + 0x24) & 0x7fff) * 2 + iVar6
                         );
          uVar7 = DAT_0803f5d0;
          if (uVar8 == DAT_0803f5ac) {
LAB_0803f5c6:
                    /* WARNING: Subroutine does not return */
            ask_question(uVar7);
          }
          uVar9 = DAT_0803f5bc;
          if ((int)uVar8 <= (int)DAT_0803f5ac) {
            uVar9 = DAT_0803f5ac - 7;
          }
          uVar7 = DAT_0803f5c0;
          if (uVar8 == uVar9) goto LAB_0803f5c6;
        }
        else {
          iVar6 = FUN_08072ecc(*(ushort *)
                                (((*param_1 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                                 iVar4 * ((*param_1 & 0x1ff) >> 8) + iVar3 + 0x24) & 0x7fff,0);
          if (iVar6 != 0) {
            uVar7 = 0x7e;
            goto LAB_0803f6e0;
          }
        }
      }
    }
  }
  uVar7 = 0;
LAB_0803f6e0:
  return CONCAT44(in_lr,uVar7);
}


// ===== 080384E0 FUN_080384e0

undefined8 FUN_080384e0(ushort *param_1)

{
  char cVar1;
  short sVar2;
  undefined4 uVar3;
  int iVar4;
  int iVar5;
  undefined4 in_lr;
  
  iVar4 = DAT_08038510 * (1 - ((byte)*param_1 & 1)) + DAT_0803850c;
  if ((*(byte *)(iVar4 + 0x1c) & 0x3f) != 0 || *(char *)(iVar4 + 0x1b) < '\0') {
    iVar4 = 0;
    iVar5 = DAT_0803850c + DAT_08038564;
    do {
      cVar1 = *(char *)(iVar4 + ((int)((uint)(byte)*param_1 << 0x1f) >> 0x1f) * -0xb + iVar5);
      if (((cVar1 != -1) && (sVar2 = FUN_0800ddc0(cVar1,3), sVar2 != 0)) &&
         (sVar2 = FUN_08010814(cVar1,3,(*param_1 & 0x1ff) >> 1), sVar2 != 0)) {
        uVar3 = 1;
        goto LAB_0803855c;
      }
      iVar4 = iVar4 + 1;
    } while (iVar4 < 5);
  }
  uVar3 = 0;
LAB_0803855c:
  return CONCAT44(in_lr,uVar3);
}


// ===== 0802F4BC FUN_0802f4bc

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0802f4bc(ushort *param_1)

{
  undefined1 uVar1;
  short sVar2;
  short sVar3;
  int iVar4;
  int iVar5;
  undefined4 uVar6;
  uint uVar7;
  code *UNRECOVERED_JUMPTABLE;
  undefined1 auStack_114 [256];
  
  if ((*(ushort *)(iRam0802f518 + 0x7c0) & 0x3ff) >> 2 == 0) {
    uVar7 = (uint)*(ushort *)
                   ((*(ushort *)
                      (((*param_1 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                       iRam0802f524 * ((*param_1 & 0x1ff) >> 8) + iRam0802f520 + 0x24) & 0x7fff) * 2
                   + iRam0802f51c);
    iVar4 = iRam0802f55c;
    iVar5 = iRam0802f558;
    if (uVar7 != uRam0802f528) {
      if ((int)uRam0802f528 < (int)uVar7) {
        iVar4 = iRam0802f574;
        iVar5 = FUN_0802f56e;
        if (uVar7 == uRam0802f53c) goto code_r0x0802f564;
        if (uVar7 == uRam0802f53c + 1) {
                    /* WARNING: Subroutine does not return */
          replace_string_in_template2(auStack_114,DAT_0802f5ac,DAT_0802f5ac + DAT_0802f5b0);
        }
      }
      else {
        iVar4 = iRam0802f54c;
        iVar5 = iRam0802f548;
        if (uVar7 == uRam0802f528 - 1) goto code_r0x0802f564;
      }
                    /* WARNING: Subroutine does not return */
      ask_question(auStack_114);
    }
code_r0x0802f564:
                    /* WARNING: Subroutine does not return */
    replace_string_in_template2(auStack_114,iVar5,iVar5 + iVar4);
  }
  iVar5 = FUN_08009094(0xf0);
  iVar4 = iRam0802f624;
  if (iVar5 != 0) {
    uVar1 = *(undefined1 *)(iRam0802f624 + iRam0802f628);
    sVar2 = FUN_08010814(uVar1,3,(*param_1 & 0x1ff) >> 1);
    uVar7 = (uint)*(ushort *)
                   ((*(ushort *)
                      (((*param_1 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                       iRam0802f630 * ((*param_1 & 0x1ff) >> 8) + iVar4 + 0x24) & 0x7fff) * 2 +
                   iRam0802f62c);
    if (uVar7 == uRam0802f634) {
      uVar6 = 3;
code_r0x0802f65c:
      sVar3 = FUN_0800ddc0(uVar1,uVar6);
      if (sVar3 != 0) goto code_r0x0802f678;
    }
    else {
      if ((int)uRam0802f634 < (int)uVar7) {
        if (uVar7 == uRam0802f648) {
          uVar6 = 4;
          goto code_r0x0802f65c;
        }
        if ((uVar7 == uRam0802f648 + 1) && (sVar3 = FUN_0800ddc0(uVar1,6), sVar3 == 0)) {
          sVar2 = 0;
        }
      }
      else if (uVar7 == uRam0802f634 - 1) {
        uVar6 = 5;
        goto code_r0x0802f65c;
      }
code_r0x0802f678:
      if (sVar2 != 0) {
        uVar7 = (uint)*(ushort *)
                       ((*(ushort *)
                          (((*param_1 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                           iRam0802f6c4 * ((*param_1 & 0x1ff) >> 8) + iRam0802f6c0 + 0x24) & 0x7fff)
                        * 2 + iRam0802f6bc);
        if (uVar7 == uRam0802f6c8) {
          *(byte *)(param_1 + 4) = (byte)param_1[4] & 0xf0;
          FUN_08051650(param_1,uVar1);
        }
        else if (uVar7 == uRam0802f6c8 + 2) {
          *(byte *)(param_1 + 4) = (byte)param_1[4] & 0xf0;
          uVar6 = FUN_080122ec(uVar1);
          FUN_080516c8(param_1,uVar6);
        }
        uVar6 = 1;
        if ((*param_1 & 1) != 0) {
          uVar6 = uRam0802f728;
        }
        drawing_FUN_08022084(uVar6,uVar1);
        FUN_080184ec((byte)*param_1 & 1,uVar1,(*param_1 & 0x1ff) >> 1);
        uVar6 = 1;
        goto code_r0x0802f734;
      }
    }
    FUN_080e6d88(3);
  }
  uVar6 = 0;
code_r0x0802f734:
                    /* WARNING: Could not recover jumptable at 0x0802f73a. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*UNRECOVERED_JUMPTABLE)(uVar6);
  return;
}


