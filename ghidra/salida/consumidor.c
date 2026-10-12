// ===== 0807B3B4 FUN_0807b3b4

undefined8 FUN_0807b3b4(void)

{
  byte bVar1;
  byte bVar2;
  bool bVar3;
  char cVar4;
  short sVar5;
  ushort uVar6;
  ushort uVar7;
  uint uVar8;
  uint uVar9;
  code *UNRECOVERED_JUMPTABLE;
  undefined4 uVar10;
  uint uVar11;
  int iVar12;
  int iVar13;
  int iVar14;
  byte bVar15;
  uint uVar16;
  uint uVar17;
  uint *puVar18;
  int iVar19;
  char *pcVar20;
  uint uVar21;
  uint uVar22;
  undefined4 in_lr;
  undefined8 uVar23;
  undefined4 local_24;
  
  iVar12 = DAT_0807b63c;
  puVar18 = DAT_0807b518;
  iVar19 = DAT_0807b410;
  bVar15 = *(byte *)(DAT_0807b410 + 0x10);
  uVar16 = *(byte *)(DAT_0807b410 + 0x11) & 0x3f;
  uVar8 = (*(byte *)(DAT_0807b410 + 0x11) & 0x7f) >> 6;
  uVar11 = (int)((uint)*(byte *)(DAT_0807b410 + 0x14) << 0x1f) >> 0x1f;
  uVar22 = -uVar11;
  uVar21 = (uint)(*(byte *)(DAT_0807b410 + 0x14) >> 1);
  bVar1 = *(byte *)(DAT_0807b410 + 0x15);
  uVar17 = bVar1 & 0x3f;
  uVar9 = (bVar1 & 0x7f) >> 6;
  local_24 = 0;
  bVar2 = *(byte *)(DAT_0807b410 + 0xf);
  if (bVar2 == 1) {
    sVar5 = FUN_0807b270(*(byte *)(DAT_0807b63c + 4) & 3);
    puVar18 = DAT_0807b640;
    if (sVar5 == 0) goto LAB_0807b8ce;
    *DAT_0807b640 = *DAT_0807b640 & DAT_0807b644;
    *(ushort *)((int)puVar18 + 2) = (ushort)DAT_0807b648 & *(ushort *)((int)puVar18 + 2);
    uVar6 = *(ushort *)(iVar12 + 4) & 3;
    if (uVar6 != 1) {
      if (uVar6 != 2) goto LAB_0807b8ce;
      if (*(short *)((int)puVar18 + 10) != 7) {
        *(char *)(iVar19 + 0xf) = *(char *)(iVar19 + 0xf) + '\x01';
        goto LAB_0807b8ce;
      }
    }
    *(undefined2 *)((int)puVar18 + 6) = 0;
    local_24 = 1;
    goto LAB_0807b8ce;
  }
  if (1 < bVar2) {
    if (bVar2 == 2) {
      if (((*(short *)(DAT_0807b670 + 10) == 7) && (10 < uVar21)) && (uVar21 < 0x10)) {
        *(undefined2 *)(DAT_0807b670 + 6) = 0;
        local_24 = 1;
      }
      else {
        uVar16 = FUN_0807b22c(bVar15 & 1,bVar15 >> 1,uVar16);
        iVar19 = DAT_0807b718;
        uVar17 = (uint)*(ushort *)(DAT_0807b718 + 6);
        iVar12 = fast_division(uVar17 * (int)*(short *)(DAT_0807b718 + 0xc),0xc);
        iVar19 = fast_division(uVar17 * (int)*(short *)(iVar19 + 0xe),0xc);
        bVar3 = false;
        if (5 < uVar17) {
          uVar17 = 0xb - uVar17 & 0xffff;
        }
        uVar11 = (int)(uVar11 | uVar22) >> 0x1f & 0x40;
        if (uVar8 != uVar9) {
          if (uVar8 != 0) {
            uVar11 = uVar11 + 0x20;
          }
          bVar3 = true;
        }
        iVar13 = fast_division(uVar17 * 0xaa,6);
        if (*(ushort *)(DAT_0807b718 + 10) == 7) {
          uVar6 = 0x400;
        }
        else {
          uVar6 = ((*(ushort *)(DAT_0807b718 + 10) & 0xf) + 1) * 0x1000 | 0x400;
        }
        if ((char)bVar1 < '\0') {
          uVar7 = 0x3a;
        }
        else {
          uVar7 = 0x38;
        }
        if (bVar3) {
          iVar14 = fast_division((uint)*(ushort *)(DAT_0807b718 + 6) << 5,0xc);
          uVar11 = uVar11 + iVar14;
        }
        FUN_080e3574((uVar16 & 0xffff) + iVar12 & 0xffff |
                     ((uVar16 >> 0x10) + iVar19) * 0x10000 + 0x2000000,DAT_0807b790,uVar6 | uVar7,
                     uVar11 | (0x100 - iVar13) * 0x10000);
        iVar19 = DAT_0807b794;
        *(ushort *)(DAT_0807b794 + 4) = *(ushort *)(DAT_0807b794 + 4) | 0x2000;
        uVar11 = ((*DAT_0807b798 & 0x1f) >> 3) + *(ushort *)(iVar19 + 6) + 1;
        *(short *)(iVar19 + 6) = (short)uVar11;
        if (0xb < (uVar11 & 0xffff)) {
          *(undefined2 *)(iVar19 + 6) = 0;
          *(char *)(DAT_0807b79c + 0xf) = *(char *)(DAT_0807b79c + 0xf) + '\x01';
        }
      }
      goto LAB_0807b8ce;
    }
    if (bVar2 != 3) goto LAB_0807b8ce;
    uVar8 = FUN_0807b22c(uVar22,uVar21,uVar17);
    uVar11 = (int)(uVar11 | uVar22) >> 0x1f & 0x40;
    if (uVar9 != 0) {
      uVar11 = uVar11 + 0x20;
    }
    if (*(ushort *)(DAT_0807b7ec + 10) == 7) {
      uVar6 = 0x400;
    }
    else {
      uVar6 = ((*(ushort *)(DAT_0807b7ec + 10) & 0xf) + 1) * 0x1000 | 0x400;
    }
    if ((char)bVar1 < '\0') {
      uVar7 = 0x3a;
    }
    else {
      uVar7 = 0x38;
    }
    FUN_080e3574(((uVar8 >> 0x10) + 0x200) * 0x10000 | uVar8 & 0xffff,DAT_0807b858,uVar6 | uVar7,
                 uVar11 | 0x1000000);
    iVar19 = DAT_0807b85c;
    *(ushort *)(DAT_0807b85c + 4) = *(ushort *)(DAT_0807b85c + 4) | 0x2000;
    *(char *)(DAT_0807b860 + 0xf) = *(char *)(DAT_0807b860 + 0xf) + '\x01';
    local_24 = 1;
    pcVar20 = (char *)(iVar19 + 0x29);
    if ((*pcVar20 != '\0') && (*pcVar20 != '\x05')) goto LAB_0807b8ce;
    FUN_08008cf4();
    iVar12 = FUN_08008c6c();
    if (iVar12 != 0xff) goto LAB_0807b8ce;
    if (*pcVar20 == '\0') {
      bVar15 = (*(byte *)(DAT_0807b87c + 0x1c) & 0x3f) << 1 | *(byte *)(DAT_0807b87c + 0x1b) >> 7;
      if (bVar15 == 0) {
        *(undefined1 *)(iVar19 + 0x2a) = 0;
        cVar4 = *pcVar20 + '\x01';
LAB_0807b8ca:
        *pcVar20 = cVar4;
        goto LAB_0807b8ce;
      }
    }
    else {
      if (*pcVar20 != '\x05') goto LAB_0807b8ce;
      bVar15 = (*(byte *)(DAT_0807b8b4 + DAT_0807b8bc) & 0x3f) << 1 |
               *(byte *)(DAT_0807b8b4 + DAT_0807b8b8) >> 7;
      if (bVar15 == 0) {
        *(undefined1 *)(iVar19 + 0x2a) = 0;
        cVar4 = *pcVar20 + -1;
        goto LAB_0807b8ca;
      }
    }
    *(byte *)(iVar19 + 0x2a) = bVar15 - 1;
    goto LAB_0807b8ce;
  }
  if (bVar2 != 0) goto LAB_0807b8ce;
  if (uVar21 < 0x10) {
    UNRECOVERED_JUMPTABLE = *(code **)(uVar21 * 4 + DAT_0807b43c);
                    /* WARNING: Could not recover jumptable at 0x0807b438. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    uVar23 = (*UNRECOVERED_JUMPTABLE)
                       (UNRECOVERED_JUMPTABLE,DAT_0807b43c,uVar11 * -0x80 | uVar21 | uVar17 << 8);
    return uVar23;
  }
  iVar19 = 0;
  if (*(short *)(DAT_0807b410 + 0xc) == 0) {
    iVar19 = 7;
  }
  *(short *)((int)DAT_0807b518 + 10) = (short)iVar19;
  uVar10 = FUN_0807b22c(uVar22,uVar21,uVar17);
  *(short *)(puVar18 + 3) = (short)uVar10;
  *(short *)((int)puVar18 + 0xe) = (short)((uint)uVar10 >> 0x10);
  uVar11 = FUN_0807b22c(bVar15 & 1,bVar15 >> 1,uVar16);
  *(short *)(puVar18 + 3) = (short)puVar18[3] - (short)uVar11;
  *(short *)((int)puVar18 + 0xe) = *(short *)((int)puVar18 + 0xe) - (short)(uVar11 >> 0x10);
  uVar9 = 0;
  if ((uVar8 != 0) && (uVar9 = 0x20, (bVar15 & 1) != 0)) {
    uVar9 = 0x60;
  }
  if ((uVar21 < 0xc) || (uVar21 == 0xf)) {
    if ((*(short *)(DAT_0807b58c + 10) != 7) || (uVar21 == 0xf)) {
      uVar11 = ((uVar11 >> 0x10) + 0x200) * 0x10000 | uVar11 & 0xffff;
      if (iVar19 == 7) {
        uVar8 = 0x400;
      }
      else {
        uVar8 = (iVar19 + 1) * 0x1000 | 0x400;
      }
      if ((char)bVar1 < '\0') {
        uVar16 = 0x3a;
      }
      else {
LAB_0807b59e:
        uVar16 = 0x38;
      }
LAB_0807b5a0:
      FUN_080e3574(uVar11,DAT_0807b5e4,uVar8 | uVar16,uVar9 | 0x1000000);
    }
LAB_0807b5b6:
    puVar18 = DAT_0807b5e8;
    *(ushort *)(DAT_0807b5e8 + 1) = (ushort)DAT_0807b5e8[1] | 0x2000;
    *(undefined1 *)(DAT_0807b5ec + 0xf) = 2;
  }
  else {
    if ((2 < (*(ushort *)(DAT_0807b51c + 4) & 3)) || ((*(ushort *)(DAT_0807b51c + 4) & 3) == 0)) {
      if (*(short *)(DAT_0807b54c + 10) != 7) {
        uVar11 = ((uVar11 >> 0x10) + 0x200) * 0x10000 | uVar11 & 0xffff;
        if (iVar19 == 7) {
          uVar8 = 0x400;
        }
        else {
          uVar8 = (iVar19 + 1) * 0x1000 | 0x400;
        }
        if (-1 < (char)bVar1) goto LAB_0807b59e;
        uVar16 = 0x3a;
        goto LAB_0807b5a0;
      }
      goto LAB_0807b5b6;
    }
    *(undefined1 *)(DAT_0807b520 + 0xf) = 1;
    puVar18 = DAT_0807b518;
  }
  *puVar18 = *puVar18 & DAT_0807b5f0;
  *(undefined2 *)((int)puVar18 + 6) = 0;
  FUN_080e6d88(5);
LAB_0807b8ce:
  return CONCAT44(in_lr,local_24);
}


// ===== 0807D41C FUN_0807d41c

undefined8 FUN_0807d41c(void)

{
  byte bVar1;
  byte bVar2;
  byte bVar3;
  uint *puVar4;
  byte bVar5;
  byte bVar6;
  undefined1 uVar7;
  short sVar8;
  ushort uVar9;
  ushort uVar10;
  uint uVar11;
  code *UNRECOVERED_JUMPTABLE;
  undefined4 uVar12;
  int iVar13;
  int iVar14;
  int iVar15;
  uint uVar16;
  uint uVar17;
  undefined4 in_lr;
  undefined8 uVar18;
  undefined4 local_24;
  
  iVar14 = DAT_0807d6d8;
  iVar13 = DAT_0807d55c;
  iVar15 = DAT_0807d46c;
  bVar5 = *(byte *)(DAT_0807d46c + 0x10) & 1;
  bVar3 = *(byte *)(DAT_0807d46c + 0x10) >> 1;
  bVar6 = *(byte *)(DAT_0807d46c + 0x11) & 0x3f;
  uVar11 = *(byte *)(DAT_0807d46c + 0x14) & 1;
  uVar17 = (uint)(*(byte *)(DAT_0807d46c + 0x14) >> 1);
  bVar1 = *(byte *)(DAT_0807d46c + 0x15);
  uVar16 = bVar1 & 0x3f;
  local_24 = 0;
  bVar2 = *(byte *)(DAT_0807d46c + 0xf);
  if (bVar2 == 1) {
    sVar8 = FUN_0807d24c(*(byte *)(DAT_0807d6d8 + 4) & 3);
    puVar4 = DAT_0807d6dc;
    if (sVar8 != 0) {
      *DAT_0807d6dc = *DAT_0807d6dc & DAT_0807d6e0;
      *(ushort *)((int)puVar4 + 2) = (ushort)DAT_0807d6e4 & *(ushort *)((int)puVar4 + 2);
      uVar9 = *(ushort *)(iVar14 + 4) & 3;
      if (uVar9 == 1) {
        *(undefined2 *)((int)puVar4 + 6) = 0;
        local_24 = 1;
      }
      else {
        if (uVar9 == 2) {
          if (*(short *)((int)puVar4 + 10) == 7) {
            *(undefined2 *)((int)puVar4 + 6) = 0;
            local_24 = 1;
            goto LAB_0807d9e2;
          }
          *(char *)(iVar15 + 0xf) = *(char *)(iVar15 + 0xf) + '\x01';
        }
        *(undefined2 *)((int)puVar4 + 6) = 0;
      }
    }
    goto LAB_0807d9e2;
  }
  if (1 < bVar2) {
    if (bVar2 == 2) {
      if (((*(short *)(DAT_0807d728 + 10) != 7) || (uVar17 < 0xb)) || (0xf < uVar17)) {
        uVar11 = FUN_0807d208(bVar5,bVar3,bVar6);
        iVar15 = DAT_0807d7dc;
        uVar16 = uVar11 >> 0x10;
        if (0 < *(short *)(DAT_0807d7dc + 0xe)) {
          uVar16 = uVar16 + *(ushort *)(DAT_0807d7dc + 0xe) & 0xffff;
        }
        uVar9 = *(ushort *)(DAT_0807d7dc + 6);
        uVar17 = (uVar9 & 0x3fff) * 4;
        if (0 < *(short *)(DAT_0807d7dc + 0xe)) {
          uVar17 = uVar17 + 0x10;
        }
        iVar13 = fast_division(0x100,(int)*(short *)(DAT_0807d7dc + 0xe));
        if (iVar13 < 0) {
          iVar13 = -iVar13;
        }
        iVar13 = fast_division((int)((uint)*(ushort *)((uVar17 & 0x7f) * 2 + DAT_0807d7e0) *
                                    -0x10000) >> 0x10,(int)(short)iVar13);
        iVar14 = fast_division((uint)uVar9 * (int)*(short *)(iVar15 + 0xc),0xc);
        uVar9 = *(ushort *)(iVar15 + 10);
        if (uVar9 == 7) {
          uVar9 = 0x400;
        }
        else {
          uVar9 = ((uVar9 & 0xf) + 1) * 0x1000 | 0x400;
        }
        if ((char)bVar1 < '\0') {
          uVar10 = 0x39;
        }
        else {
          uVar10 = 0x36;
        }
                    /* WARNING: Subroutine does not return */
        FUN_080e2df4((uVar16 + iVar13) * 0x10000 | iVar14 + (uVar11 & 0xffff) & 0xffff,DAT_0807d824,
                     uVar9 | uVar10);
      }
      *(undefined2 *)(DAT_0807d728 + 6) = 0;
      local_24 = 1;
    }
    else if (bVar2 == 3) {
      uVar12 = FUN_0807d208(uVar11,uVar17,uVar16);
      if (*(ushort *)(DAT_0807d8c0 + 10) == 7) {
        uVar9 = 0x400;
      }
      else {
        uVar9 = ((*(ushort *)(DAT_0807d8c0 + 10) & 0xf) + 1) * 0x1000 | 0x400;
      }
      if ((char)bVar1 < '\0') {
        uVar10 = 0x39;
      }
      else {
        uVar10 = 0x36;
      }
                    /* WARNING: Subroutine does not return */
      FUN_080e2df4(uVar12,DAT_0807d904,uVar9 | uVar10);
    }
    goto LAB_0807d9e2;
  }
  if (bVar2 != 0) goto LAB_0807d9e2;
  if (uVar17 < 0x10) {
    UNRECOVERED_JUMPTABLE = *(code **)(uVar17 * 4 + DAT_0807d498);
                    /* WARNING: Could not recover jumptable at 0x0807d494. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    uVar18 = (*UNRECOVERED_JUMPTABLE)
                       (UNRECOVERED_JUMPTABLE,DAT_0807d498,uVar11 << 7 | uVar17 | uVar16 << 8);
    return uVar18;
  }
  iVar15 = 0;
  if (*(short *)(DAT_0807d46c + 0xc) == 0) {
    iVar15 = 7;
  }
  *(short *)(DAT_0807d55c + 10) = (short)iVar15;
  uVar12 = FUN_0807d208(uVar11,uVar17,uVar16);
  *(short *)(iVar13 + 0xc) = (short)uVar12;
  *(short *)(iVar13 + 0xe) = (short)((uint)uVar12 >> 0x10);
  uVar11 = FUN_0807d208(bVar5,bVar3,bVar6);
  *(short *)(iVar13 + 0xc) = *(short *)(iVar13 + 0xc) - (short)uVar11;
  *(short *)(iVar13 + 0xe) = (*(short *)(iVar13 + 0xe) + -0x10) - (short)(uVar11 >> 0x10);
  if ((uVar17 < 0xc) || (uVar17 == 0xf)) {
    if ((*(short *)(DAT_0807d608 + 10) != 7) || (uVar17 == 0xf)) {
      if (iVar15 == 7) {
        uVar16 = 0x400;
      }
      else {
        uVar16 = (iVar15 + 1) * 0x1000 | 0x400;
      }
      if ((char)bVar1 < '\0') {
        uVar17 = 0x39;
      }
      else {
        uVar17 = 0x36;
      }
                    /* WARNING: Subroutine does not return */
      FUN_080e2df4(uVar11 & 0xffff | (uVar11 >> 0x10) << 0x10,DAT_0807d644,uVar16 | uVar17);
    }
LAB_0807d674:
    uVar7 = 2;
    iVar15 = DAT_0807d698;
  }
  else {
    if ((2 < (*(ushort *)(DAT_0807d560 + 4) & 3)) || ((*(ushort *)(DAT_0807d560 + 4) & 3) == 0)) {
      if (*(short *)(DAT_0807d590 + 10) != 7) {
        if (iVar15 == 7) {
          uVar16 = 0x400;
        }
        else {
          uVar16 = (iVar15 + 1) * 0x1000 | 0x400;
        }
        if ((char)bVar1 < '\0') {
          uVar17 = 0x39;
        }
        else {
          uVar17 = 0x36;
        }
                    /* WARNING: Subroutine does not return */
        FUN_080e2df4(uVar11 & 0xffff | (uVar11 >> 0x10) << 0x10,DAT_0807d5cc,uVar16 | uVar17);
      }
      goto LAB_0807d674;
    }
    uVar7 = 1;
    iVar15 = DAT_0807d564;
  }
  *(undefined1 *)(iVar15 + 0xf) = uVar7;
  puVar4 = DAT_0807d694;
  *DAT_0807d694 = *DAT_0807d694 & DAT_0807d69c;
  *(undefined2 *)((int)puVar4 + 6) = 0;
  FUN_080e6d88(5);
LAB_0807d9e2:
  return CONCAT44(in_lr,local_24);
}


// ===== 0807FEB4 FUN_0807feb4

longlong FUN_0807feb4(void)

{
  uint in_lr;
  longlong lVar1;
  
  if (5 < *(byte *)(DAT_0807ff10 + 0xf)) {
    return (ulonglong)in_lr << 0x20;
  }
                    /* WARNING: Could not recover jumptable at 0x0807ff0e. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  lVar1 = (**(code **)((uint)*(byte *)(DAT_0807ff10 + 0xf) * 4 + DAT_0807ff14))();
  return lVar1;
}


