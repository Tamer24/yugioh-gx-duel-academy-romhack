// ===== 08066B24 FUN_08066b24

void FUN_08066b24(void)

{
  byte bVar1;
  
  bVar1 = *(byte *)(DAT_08066b4c + 0xb);
  if (5 < bVar1) {
    FUN_080674ca();
  }
                    /* WARNING: Could not recover jumptable at 0x08066b48. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (**(code **)((uint)bVar1 * 4 + DAT_08066b50))();
  return;
}


// ===== 08068C8C FUN_08068c8c

void FUN_08068c8c(void)

{
  ushort uVar1;
  uint *puVar2;
  uint uVar3;
  uint uVar4;
  uint uVar5;
  undefined4 uVar6;
  uint uVar7;
  int iVar8;
  int unaff_r7;
  code *UNRECOVERED_JUMPTABLE;
  
  cleanup_card_actions();
  puVar2 = DAT_08068cf0;
  uVar3 = *DAT_08068cf0;
  uVar4 = (uint)*(ushort *)
                 ((*(ushort *)
                    (((uVar3 & 0x1fffff) >> 0xd & 0x7f) * 0x50 +
                     DAT_08068cf4 * ((uVar3 & 0x1fffff) >> 0x14) + DAT_08068cec + 0x24) & 0x7fff) *
                  2 + DAT_08068ce8);
  if (uVar4 == DAT_08068cf8) {
    if (((DAT_08068cf0[unaff_r7 * 6 + 9] & 1) == 0) &&
       ((DAT_08068cf0[(1 - unaff_r7) * 6 + 9] & 1) != 0)) {
      FUN_0801aaa4(unaff_r7,(uVar3 & 0x1fffff) >> 0xd);
      uVar3 = *puVar2;
      uVar6 = 0xb;
LAB_08068ed2:
      uVar3 = (uVar3 & 0x1fffff) >> 0xd;
      FUN_0801a5bc(unaff_r7,uVar3,uVar3,uVar6);
      uVar6 = 1;
      if (unaff_r7 != 0) {
        uVar6 = DAT_08068eec;
      }
      drawing_FUN_08022084(uVar6,(*puVar2 & 0x1fffff) >> 0xd);
    }
  }
  else if ((int)DAT_08068cf8 < (int)uVar4) {
    if (uVar4 == DAT_08068d30) {
LAB_08068d4c:
      if ((*DAT_08068d80 & 1) != 0) goto LAB_0806931a;
      FUN_080234f4(unaff_r7 << 0x1f | (*DAT_08068d80 & 0x1fffff) >> 0xd | DAT_08068d84,
                   (*DAT_08068d80 & 0x1fffff) >> 0xd |
                   ((*(ushort *)((int)DAT_08068d80 + 2) & 0x1fff) >> 5) << 0x10);
    }
    else if ((int)DAT_08068d30 < (int)uVar4) {
      if (uVar4 == DAT_08068d48) goto LAB_08068d4c;
      if (uVar4 == DAT_08068d48 + 0x3a) {
        if ((*DAT_08068cf0 & 1) != 0) goto LAB_0806931a;
        if (-1 < (int)((uint)*(byte *)(((*(ushort *)((int)DAT_08068cf0 + 2) & 0x1fff) >> 5 & 0x7f) *
                                       0x50 + DAT_08068cf4 *
                                              ((*(ushort *)((int)DAT_08068cf0 + 2) & 0x1fff) >> 0xc)
                                       + DAT_08068cec + 0x33) * 0x4000000)) {
          FUN_0801aa84(unaff_r7,(uVar3 & 0x1fffff) >> 0xd);
          FUN_0801a36c(unaff_r7,(*(ushort *)((int)puVar2 + 2) & 0x1fff) >> 5,0,0);
        }
      }
    }
    else if (uVar4 == DAT_08068d34) {
      if (((DAT_08068cf0[unaff_r7 * 6 + 9] & 1) == 0) &&
         ((DAT_08068cf0[(1 - unaff_r7) * 6 + 9] & 1) != 0)) {
        FUN_0801aaa4(unaff_r7,(uVar3 & 0x1fffff) >> 0xd);
        uVar3 = *puVar2;
        uVar6 = 0xc;
        goto LAB_08068ed2;
      }
    }
    else if (uVar4 == DAT_08068d34 + 0xb0) goto LAB_08068d88;
  }
  else {
    if (uVar4 == DAT_08068cf8 - 0xd3) {
LAB_08068d88:
      FUN_0800e158((uVar3 & 0x1fffff) >> 0xd,0xe);
      return;
    }
    if ((int)(DAT_08068cf8 - 0xd3) < (int)uVar4) {
      if (((uVar4 == DAT_08068d10) || (uVar4 == DAT_08068d10 + 7)) &&
         ((DAT_08068e4c[unaff_r7 * 6 + 9] & 1) != 0)) {
        uVar3 = *(ushort *)((int)DAT_08068e4c + 2) & 0x1fff;
        uVar5 = uVar3 >> 5;
        uVar4 = *DAT_08068e4c & 0x1fffff;
        uVar7 = uVar4 >> 0xd;
        FUN_080234f4(unaff_r7 << 0x1f | (*DAT_08068e4c & 0x1fffff) >> 0xd | 0x1c800000,
                     (*(uint *)((uVar5 & 0x7f) * 0x50 + (uVar3 >> 0xc) * DAT_08068e54 + DAT_08068e50
                               + 0x30) >> 0xc & 0xff) << 8 | uVar5 |
                     uVar7 << 0x10 |
                     (*(uint *)((uVar7 & 0x7f) * 0x50 + (uVar4 >> 0x14) * DAT_08068e54 +
                                DAT_08068e50 + 0x30) >> 0xc) << 0x18);
      }
    }
    else if (uVar4 == DAT_08068cfc) goto LAB_08068d4c;
  }
  iVar8 = DAT_08068fbc;
  puVar2 = DAT_08068fb4;
  if ((*DAT_08068fb4 & 1) != 0) goto LAB_0806931a;
  uVar3 = (uint)*(ushort *)((int)DAT_08068fb4 + 2);
  uVar4 = (uint)*(ushort *)
                 ((*(ushort *)
                    (((uVar3 & 0x1fff) >> 5 & 0x7f) * 0x50 +
                     ((uVar3 & 0x1fff) >> 0xc) * DAT_08068fbc + DAT_08068fc0 + 0x24) & 0x7fff) * 2 +
                 DAT_08068fb8);
  if (uVar4 == DAT_08068fc4) {
LAB_08069138:
    if ((DAT_08068fb4[(1 - unaff_r7) * 6 + 9] & 1) == 0) goto LAB_0806931a;
    uVar5 = (uint)*(ushort *)((int)DAT_08068fb4 + 2);
    uVar3 = (1 - unaff_r7) * -0x80000000 | (uVar5 & 0x1fff) >> 5 | 0x1c800000;
    uVar7 = (*DAT_08068fb4 & 0x1fffff) >> 0xd;
    uVar4 = (*(uint *)(((uVar5 & 0x1fff) >> 5 & 0x7f) * 0x50 +
                       DAT_080691cc * ((uVar5 & 0x1fff) >> 0xc) + DAT_08068fc0 + 0x30) >> 0xc & 0xff
            ) << 8 | uVar7;
    uVar5 = ((uVar5 & 0x1fff) >> 5) << 0x10 |
            (*(uint *)((uVar7 & 0x7f) * 0x50 + DAT_080691cc * ((*DAT_08068fb4 & 0x1fffff) >> 0x14) +
                       DAT_08068fc0 + 0x30) >> 0xc) << 0x18;
  }
  else if ((int)DAT_08068fc4 < (int)uVar4) {
    if (uVar4 == DAT_08069004) goto LAB_08069114;
    if ((int)uVar4 <= (int)DAT_08069004) {
      if (uVar4 == DAT_08069004 - 0x77) {
        iVar8 = 1 - unaff_r7;
        if (((DAT_08068fb4[iVar8 * 6 + 9] & 1) != 0) || ((DAT_08068fb4[unaff_r7 * 6 + 9] & 1) == 0))
        goto LAB_0806931a;
        FUN_0801aaa4(iVar8,(uVar3 & 0x1fff) >> 5);
        uVar3 = (*(ushort *)((int)puVar2 + 2) & 0x1fff) >> 5;
        FUN_0801a5bc(iVar8,uVar3,uVar3,0xb);
        uVar6 = 1;
        if (unaff_r7 != 1) {
          uVar6 = DAT_08069228;
        }
        uVar1 = *(ushort *)((int)puVar2 + 2);
      }
      else {
        if (((uVar4 != DAT_08069004 - 0x74) ||
            (iVar8 = 1 - unaff_r7, (DAT_08068fb4[iVar8 * 6 + 9] & 1) != 0)) ||
           ((DAT_08068fb4[unaff_r7 * 6 + 9] & 1) == 0)) goto LAB_0806931a;
        FUN_0801aaa4(iVar8,(uVar3 & 0x1fff) >> 5);
        uVar3 = (*(ushort *)((int)puVar2 + 2) & 0x1fff) >> 5;
        FUN_0801a5bc(iVar8,uVar3,uVar3,0xc);
        uVar6 = 1;
        if (unaff_r7 != 1) {
          uVar6 = DAT_08069284;
        }
        uVar1 = *(ushort *)((int)puVar2 + 2);
      }
      drawing_FUN_08022084(uVar6,(uVar1 & 0x1fff) >> 5);
      goto LAB_0806931a;
    }
    if (uVar4 != DAT_0806901c) {
      if ((int)DAT_0806901c < (int)uVar4) {
        if ((uVar4 == DAT_08069030) &&
           (-1 < (int)((uint)*(byte *)(((*DAT_08068fb4 & 0x1fffff) >> 0xd & 0x7f) * 0x50 +
                                       ((*DAT_08068fb4 & 0x1fffff) >> 0x14) * DAT_08068fbc +
                                       DAT_08069330 + 0x33) * 0x4000000))) {
          FUN_0801aa84(unaff_r7,(uVar3 & 0x1fff) >> 5);
          FUN_0801a36c(1 - unaff_r7,(*puVar2 & 0x1fffff) >> 0xd,0,0);
        }
        goto LAB_0806931a;
      }
      if (uVar4 != DAT_08069020) goto LAB_0806931a;
    }
LAB_08069060:
    uVar3 = (1 - unaff_r7) * -0x80000000 |
            (*(ushort *)((int)DAT_08068fb4 + 2) & 0x1fff) >> 5 | DAT_08069080;
    uVar4 = (*DAT_08068fb4 & 0x1fffff) >> 0xd;
    uVar5 = ((*(ushort *)((int)DAT_08068fb4 + 2) & 0x1fff) >> 5) << 0x10;
  }
  else {
    if (uVar4 != DAT_08068fc4 - 0xa4) {
      if ((int)uVar4 <= (int)(DAT_08068fc4 - 0xa4)) {
        if (uVar4 != DAT_08068fc8) {
          if ((uVar4 == DAT_08068fcc) &&
             (-1 < (int)((uint)*(byte *)(((uVar3 & 0x1fff) >> 5 & 0x7f) * 0x50 +
                                         ((uVar3 & 0x1fff) >> 0xc) * DAT_08068fbc + DAT_08069110 +
                                        0x33) * 0x4000000))) {
            FUN_0801aaa4(1 - unaff_r7,(uVar3 & 0x1fff) >> 5);
            uVar4 = (uint)*(ushort *)((int)puVar2 + 2);
            uVar3 = (*(uint *)(((uVar4 & 0x1fff) >> 5 & 0x7f) * 0x50 +
                               ((uVar4 & 0x1fff) >> 0xc) * iVar8 + DAT_08069110 + 0x30) & 0xfffff)
                    >> 0xc & 0x7f;
            if ((uVar3 == 0) || (uVar3 == 0x11)) {
              uVar3 = (uVar4 & 0x1fff) >> 5;
              send_card_to_graveyard(uVar3,(1U - unaff_r7 & 1) << 0xf | 0x41,uVar3);
              return;
            }
          }
          goto LAB_0806931a;
        }
        goto LAB_08069060;
      }
      if (uVar4 == DAT_08068fe0) {
        FUN_0800e158((uVar3 & 0x1fff) >> 5,0xe);
        return;
      }
      if (uVar4 != DAT_08068fe0 + 6) goto LAB_0806931a;
      goto LAB_08069138;
    }
LAB_08069114:
    uVar3 = (1 - unaff_r7) * -0x80000000 |
            (*(ushort *)((int)DAT_08068fb4 + 2) & 0x1fff) >> 5 | DAT_08069134;
    uVar4 = (*DAT_08068fb4 & 0x1fffff) >> 0xd;
    uVar5 = ((*(ushort *)((int)DAT_08068fb4 + 2) & 0x1fff) >> 5) << 0x10;
  }
  FUN_080234f4(uVar3,uVar4 | uVar5);
LAB_0806931a:
  process_card_actions();
                    /* WARNING: Could not recover jumptable at 0x0806932e. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*UNRECOVERED_JUMPTABLE)(1);
  return;
}


// ===== 08039460 FUN_08039460

undefined8 FUN_08039460(ushort *param_1)

{
  uint uVar1;
  int iVar2;
  undefined4 uVar3;
  int iVar4;
  uint uVar5;
  uint uVar6;
  undefined8 uVar7;
  
  iVar2 = DAT_080394a0;
  if (*(char *)(DAT_080394a4 + DAT_080394a8) == 'd') {
    if (*(short *)(DAT_08039794 + DAT_08039798) != 0) {
      cleanup_card_actions();
      uVar5 = (uint)*(ushort *)
                     ((*(ushort *)
                        (((*param_1 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                         DAT_080397a4 * ((*param_1 & 0x1ff) >> 8) + DAT_080397a0 + 0x24) & 0x7fff) *
                      2 + DAT_0803979c);
      if (uVar5 == DAT_080397a8) {
LAB_080397b6:
        uVar5 = (*(uint *)((param_1[2] & 0x7f) * 0x50 + DAT_08039858 * ((param_1[2] & 0x80) >> 7) +
                           DAT_08039854 + 0x30) & 0xfffff) >> 0xc & 0x7f;
        if ((uVar5 == 0) || (uVar5 == 0x11)) {
          uVar7 = send_card_to_graveyard
                            (param_1[2],((byte)*param_1 & 1) << 0xf | 2,(*param_1 & 0x1ff) >> 1);
          return uVar7;
        }
      }
      else {
        uVar6 = DAT_08039850;
        if ((int)uVar5 <= (int)DAT_080397a8) {
          uVar6 = DAT_080397ac;
        }
        if (uVar5 == uVar6) goto LAB_080397b6;
      }
      uVar5 = (*(uint *)((param_1[3] & 0x7f) * 0x50 + DAT_08039858 * ((param_1[3] & 0x80) >> 7) +
                         DAT_08039854 + 0x30) & 0xfffff) >> 0xc & 0x7f;
      if ((uVar5 == 0) || (uVar5 == 0x11)) {
        uVar7 = send_card_to_graveyard
                          (param_1[3],((byte)*param_1 & 1) << 0xf | 2,(*param_1 & 0x1ff) >> 1);
        return uVar7;
      }
      process_card_actions();
      uVar3 = 10;
      goto LAB_0803985e;
    }
  }
  else if (*(char *)(DAT_080394a4 + DAT_080394a8) == -0x80) {
    if ((*param_1 & 1) != 0) {
      *(undefined2 *)(DAT_080394ac + DAT_080394a8 + 0x50) = 1;
      uVar3 = 100;
      goto LAB_0803985e;
    }
    uVar6 = (uint)*param_1;
    uVar5 = (uint)*(ushort *)
                   ((*(ushort *)
                      (((uVar6 & 0x1ff) >> 1 & 0x7f) * 0x50 + ((uVar6 & 0x1ff) >> 8) * DAT_08039500
                       + DAT_08039504 + 0x24) & 0x7fff) * 2 + DAT_080394fc);
    if (uVar5 != DAT_08039508) {
      uVar1 = DAT_0803950c;
      if ((int)DAT_08039508 < (int)uVar5) {
        if (uVar5 == DAT_0803952c) {
          if ((*DAT_08039580 >> 8 == 0x4a) && ((*(byte *)(DAT_08039584 + 1) & 1) != 0)) {
            iVar4 = *(int *)((*(ushort *)
                               (((uVar6 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                                ((uVar6 & 0x1ff) >> 8) * DAT_08039500 + DAT_0803958c + 0x24) &
                             0x7fff) * 4 + DAT_08039588);
            iVar2 = DAT_08039590;
          }
          else {
            iVar4 = *(int *)((*(ushort *)
                               (((uVar6 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                                DAT_0803962c * ((uVar6 & 0x1ff) >> 8) + DAT_08039628 + 0x24) &
                             0x7fff) * 4 + DAT_08039624);
            iVar2 = DAT_08039630;
          }
          uVar7 = replace_string_in_template2
                            (&stack0xffffffe0 + DAT_080394a0,DAT_08039634,iVar4 + iVar2);
          return uVar7;
        }
        uVar1 = DAT_0803952c + 0xd5;
      }
      if (uVar5 != uVar1) goto LAB_0803985c;
    }
    *(undefined2 *)(DAT_08039530 + DAT_08039534) = 1;
    uVar3 = 100;
    goto LAB_0803985e;
  }
LAB_0803985c:
  uVar3 = 0;
LAB_0803985e:
  return CONCAT44(*(undefined4 *)(&stack0x000001fc + iVar2),uVar3);
}


// ===== 08071778 FUN_08071778

undefined4 FUN_08071778(byte *param_1)

{
  uint *puVar1;
  uint uVar2;
  uint uVar3;
  undefined4 in_lr;
  
  puVar1 = DAT_08071800;
  *DAT_08071800 = *DAT_08071800 & DAT_08071804 | (uint)*param_1 << 0xd;
  *(ushort *)((int)puVar1 + 2) =
       (ushort)DAT_08071808 & *(ushort *)((int)puVar1 + 2) | (ushort)param_1[1] << 5;
  *(byte *)puVar1 = (byte)*puVar1 & 0xfe | param_1[2] & 1;
  FUN_080205e0(puVar1,1,0);
  uVar3 = puVar1[8];
  uVar2 = puVar1[0xe];
  *(ushort *)(param_1 + 2) =
       *(ushort *)(param_1 + 2) & 7 | (ushort)((DAT_0807180c & uVar3 - uVar2) << 3);
  param_1[4] = (byte)(uVar3 - uVar2 >> 0xd);
  uVar2 = (byte)puVar1[9] & 1;
  param_1[2] = param_1[2] & 0xf9 | (byte)(uVar2 << 1);
  if ((puVar1[0xf] & 1) != 0) {
    uVar2 = uVar2 | 2;
  }
  param_1[2] = param_1[2] & 0xf9 | (byte)(uVar2 << 1);
  uVar2 = *(ushort *)
           (((*puVar1 & 0x1fffff) >> 0xd & 0x7f) * 0x50 +
            DAT_08071860 * ((*puVar1 & 0x1fffff) >> 0x14) + DAT_0807185c + 0x24) & 0x7fff;
  if (uVar2 != DAT_08071864) {
    uVar3 = DAT_0807188c;
    if ((int)uVar2 <= (int)DAT_08071864) {
      uVar3 = DAT_08071868;
    }
    if (uVar2 != uVar3) {
      return in_lr;
    }
  }
  param_1[2] = param_1[2] & 0xf9 | (byte)(((param_1[2] & 7) >> 1 | 1) << 1);
  return in_lr;
}


// ===== 08073534 FUN_08073534

undefined8 FUN_08073534(void)

{
  uint uVar1;
  int iVar2;
  uint uVar3;
  undefined4 uVar4;
  int iVar5;
  uint uVar6;
  undefined4 in_lr;
  undefined8 uVar7;
  
  iVar5 = DAT_080735a4;
  if ((*(byte *)(DAT_080735a4 + DAT_080735a8) & 4) == 0) {
    uVar1 = FUN_08076c54();
    uVar6 = uVar1 & 0xffff;
    if (uVar6 != 0xff) {
      iVar5 = (uVar1 & 0x7f) * 0x50 + DAT_080735ac * ((int)(uVar1 & 0x80) >> 7) + iVar5;
      uVar1 = *(byte *)(iVar5 + 0x31) & 0xf;
      iVar2 = FUN_08030280(1,uVar6,0);
      uVar4 = DAT_08073744;
      if (iVar2 != 0) {
        if (uVar1 < 7) {
                    /* WARNING: Could not recover jumptable at 0x080735a2. Too many branches */
                    /* WARNING: Treating indirect jump as call */
          uVar7 = (**(code **)(uVar1 * 4 + SUB_080735b0))();
          return uVar7;
        }
        uVar1 = FUN_080767a8(DAT_08073744,1,*(ushort *)(iVar5 + 0x24) & 0x7fff,0xff);
        uVar3 = FUN_080767a8(uVar4,1,*(ushort *)(iVar5 + 0x24) & 0x7fff,uVar1 & 0xffff);
        if (((uVar1 & 0xffff) != 0xff) && ((uVar3 & 0xffff) != 0xff)) {
          record_monster_reposition
                    (1,uVar6,((uVar1 & 0xff) << 0x10 | uVar3 << 0x18) >> 0x10 | DAT_08073748,0);
          uVar4 = 1;
          goto LAB_0807374e;
        }
      }
    }
  }
  uVar4 = 0;
LAB_0807374e:
  return CONCAT44(in_lr,uVar4);
}


// ===== 08067586 FUN_08067586

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_08067586(void)

{
  ushort uVar1;
  int iVar2;
  short sVar3;
  uint uVar4;
  uint uVar5;
  undefined4 uVar6;
  int iVar7;
  uint uVar8;
  undefined4 extraout_r1;
  undefined4 uVar9;
  uint *unaff_r5;
  int unaff_r7;
  code *UNRECOVERED_JUMPTABLE;
  
  do {
    FUN_08067e1a(0);
    uVar4 = *unaff_r5;
    uVar8 = (uint)*(ushort *)
                   ((*(ushort *)
                      (((uVar4 & 0x1fffff) >> 0xd & 0x7f) * 0x50 +
                       DAT_080675ec * ((uVar4 & 0x1fffff) >> 0x14) + DAT_080675e8 + 0x24) & 0x7fff)
                    * 2 + DAT_080675e4);
    if (uVar8 == DAT_080675f0) {
FUN_08067768:
      uVar6 = 0x3b;
      if (unaff_r7 != 0) {
        uVar6 = DAT_08067784;
      }
      uVar4 = *DAT_08067788;
LAB_0806777a:
      drawing_FUN_08022034(uVar6,(uVar4 & 0x1fffff) >> 0xd,0xe);
    }
    else if ((int)DAT_080675f0 < (int)uVar8) {
      if (uVar8 == DAT_08067630) {
        FUN_080234f4(unaff_r7 << 0x1f | (uVar4 & 0x1fffff) >> 0xd | DAT_08067820,
                     (uVar4 & 0x1fffff) >> 0xd |
                     ((*(ushort *)((int)unaff_r5 + 2) & 0x1fff) >> 5) << 0x10);
      }
      else if ((int)DAT_08067630 < (int)uVar8) {
        if (uVar8 == DAT_08067650) goto FUN_08067768;
        uVar5 = DAT_08067660;
        if ((int)DAT_08067650 < (int)uVar8) goto LAB_08067656;
        if ((uVar8 == DAT_08067650 - 0x20) && ((*unaff_r5 & 1) == 0)) {
          uVar6 = 0x3b;
          if (unaff_r7 != 0) {
            uVar6 = DAT_08067760;
          }
          uVar4 = (uVar4 & 0x1fffff) >> 0xd;
          uVar9 = 0x1b;
          goto LAB_08067746;
        }
      }
      else {
        if (uVar8 == DAT_08067634) {
          uVar6 = 0x3b;
          if (unaff_r7 != 0) {
            uVar6 = DAT_080676f8;
          }
          goto LAB_0806777a;
        }
        if (((uVar8 == DAT_08067638) && ((*unaff_r5 & 1) == 0)) &&
           (sVar3 = FUN_0800ddc0((*(ushort *)((int)unaff_r5 + 2) & 0x1fff) >> 5,1), sVar3 != 0)) {
          uVar6 = 0x3b;
          if (unaff_r7 != 0) {
            uVar6 = DAT_0806772c;
          }
          uVar4 = (*unaff_r5 & 0x1fffff) >> 0xd;
          uVar9 = 0xe;
          goto LAB_08067746;
        }
      }
    }
    else {
      if (uVar8 == DAT_080675f4) {
        FUN_08059478(unaff_r7,0x12,
                     (uVar4 & 0x1fffff) >> 0xd |
                     ((*(ushort *)((int)unaff_r5 + 2) & 0x1fff) >> 5) << 0x10);
        return;
      }
      if ((int)DAT_080675f4 < (int)uVar8) {
        uVar5 = DAT_08067610;
        if (uVar8 != DAT_0806760c) {
LAB_08067656:
          if (uVar8 != uVar5) goto FUN_080677a6;
        }
        goto FUN_08067768;
      }
      if (uVar8 == DAT_080675f8) {
        if (((*unaff_r5 & 1) == 0) &&
           (sVar3 = FUN_0800ddc0((*(ushort *)((int)unaff_r5 + 2) & 0x1fff) >> 5,6), sVar3 != 0)) {
          uVar6 = 0x3b;
          if (unaff_r7 != 0) {
            uVar6 = DAT_08067698;
          }
          uVar4 = (*unaff_r5 & 0x1fffff) >> 0xd;
          uVar9 = 0xe;
          goto LAB_08067746;
        }
      }
      else if (((uVar8 == DAT_080675fc) && ((*unaff_r5 & 1) == 0)) &&
              (sVar3 = FUN_0800ddc0((*(ushort *)((int)unaff_r5 + 2) & 0x1fff) >> 5,2), sVar3 != 0))
      {
        uVar6 = 0x3b;
        if (unaff_r7 != 0) {
          uVar6 = DAT_080676cc;
        }
        uVar4 = (*unaff_r5 & 0x1fffff) >> 0xd;
        uVar9 = 0xe;
LAB_08067746:
        drawing_FUN_08022034(uVar6,uVar4,uVar9);
        uVar6 = 1;
        if (unaff_r7 != 0) {
          uVar6 = DAT_08067764;
        }
        drawing_FUN_08022084(uVar6,(*unaff_r5 & 0x1fffff) >> 0xd);
      }
    }
FUN_080677a6:
    unaff_r5 = DAT_08067828;
    uVar6 = 3;
    if (unaff_r7 != 0) {
      uVar6 = DAT_08067824;
    }
    drawing_FUN_08022084(uVar6,(*DAT_08067828 & 0x1fffff) >> 0xd);
    if ((*unaff_r5 & 1) == 0) {
      uVar4 = (uint)*(ushort *)((int)unaff_r5 + 2);
      uVar8 = (uint)*(ushort *)
                     ((*(ushort *)
                        (((uVar4 & 0x1fff) >> 5 & 0x7f) * 0x50 +
                         ((uVar4 & 0x1fff) >> 0xc) * DAT_08067834 + DAT_08067830 + 0x24) & 0x7fff) *
                      2 + DAT_0806782c);
      if (uVar8 == DAT_08067838) {
        uVar6 = 0x3b;
        if (unaff_r7 != 1) {
          uVar6 = DAT_080678bc;
        }
        drawing_FUN_08022034(uVar6,(uVar4 & 0x1fff) >> 5,0xe);
      }
      else if ((int)DAT_08067838 < (int)uVar8) {
        if (uVar8 == DAT_08067854) {
          if ((int)((uint)*(byte *)(((uVar4 & 0x1fff) >> 5 & 0x7f) * 0x50 +
                                    ((uVar4 & 0x1fff) >> 0xc) * DAT_08067834 + DAT_08067830 + 0x33)
                   * 0x8000000) < 0) {
            FUN_080234f4((1 - unaff_r7) * -0x80000000 | (uVar4 & 0x1fff) >> 5 | DAT_08067954,
                         (uVar4 & 0x1fff) >> 5 | ((*unaff_r5 & 0x1fffff) >> 0xd) << 0x10);
            *(byte *)((int)unaff_r5 + 0xb) = *(byte *)((int)unaff_r5 + 0xb) + 1;
            FUN_08067586();
            FUN_08021a78(unaff_r7,1);
            *(undefined1 *)(_FUN_08067da8 + 0xb) = 2;
            FUN_08067586();
            iVar7 = handle_win_condition((uVar4 & 0x1fff) << 3,extraout_r1,(uVar4 & 0x1fff) << 0xb);
            iVar2 = DAT_08067e2c;
            if (iVar7 != 0) {
              *(byte *)(DAT_08067e2c + 0x788) = *(byte *)(DAT_08067e2c + 0x788) & 1;
              *(undefined1 *)(iVar2 + DAT_08067e30) = 0;
              *(byte *)(iVar2 + DAT_08067e34) = *(byte *)(iVar2 + DAT_08067e34) & 1;
              *(byte *)(iVar2 + DAT_08067e38) = *(byte *)(iVar2 + DAT_08067e38) & 1;
              *(uint *)(iVar2 + DAT_08067e3c) = *(uint *)(iVar2 + DAT_08067e3c) & DAT_08067e40;
              *DAT_08067e44 = (ushort)DAT_08067e48 & *DAT_08067e44 | 0x12;
              iVar2 = DAT_08067e4c;
              *(uint *)(DAT_08067e4c + DAT_08067e50) =
                   *(uint *)(DAT_08067e4c + DAT_08067e50) & DAT_08067e54;
              *(ushort *)(iVar2 + DAT_08067e58) =
                   (ushort)DAT_08067e5c & *(ushort *)(iVar2 + DAT_08067e58);
            }
                    /* WARNING: Could not recover jumptable at 0x08067e28. Too many branches */
                    /* WARNING: Treating indirect jump as call */
            (*UNRECOVERED_JUMPTABLE)(1);
            return;
          }
        }
        else if ((int)DAT_08067854 < (int)uVar8) {
          if (uVar8 == DAT_08067864) {
            uVar6 = 0x3b;
            if (unaff_r7 != 1) {
              uVar6 = DAT_08067994;
            }
            drawing_FUN_08022034(uVar6,(uVar4 & 0x1fff) >> 5,0x1c);
            uVar6 = 1;
            if (unaff_r7 != 1) {
              uVar6 = DAT_08067998;
            }
            unaff_r5 = (uint *)(uint)*(ushort *)((int)unaff_r5 + 2);
            drawing_FUN_08022084(uVar6,((uint)unaff_r5 & 0x1fff) >> 5);
          }
        }
        else if ((uVar8 == DAT_08067854 - 0x3c) &&
                (sVar3 = FUN_0800ddc0((*unaff_r5 & 0x1fffff) >> 0xd,1), sVar3 != 0)) {
          uVar6 = 0x3b;
          if (unaff_r7 != 1) {
            uVar6 = DAT_080678fc;
          }
          uVar1 = *(ushort *)((int)unaff_r5 + 2);
          goto LAB_080678de;
        }
      }
      else if (uVar8 == DAT_0806783c) {
        sVar3 = FUN_0800ddc0((*unaff_r5 & 0x1fffff) >> 0xd,2);
        if (sVar3 != 0) {
          uVar6 = 0x3b;
          if (unaff_r7 != 1) {
            uVar6 = DAT_0806788c;
          }
          uVar1 = *(ushort *)((int)unaff_r5 + 2);
LAB_080678de:
          drawing_FUN_08022034(uVar6,(uVar1 & 0x1fff) >> 5,0xe);
          uVar6 = 1;
          if (unaff_r7 != 1) {
            uVar6 = DAT_08067900;
          }
          unaff_r5 = (uint *)(uint)*(ushort *)((int)unaff_r5 + 2);
          drawing_FUN_08022084(uVar6,((uint)unaff_r5 & 0x1fff) >> 5);
        }
      }
      else if (uVar8 == DAT_0806783c + 0x10) {
        FUN_08059478(1 - unaff_r7,0x12,
                     (uVar4 & 0x1fff) >> 5 | ((*unaff_r5 & 0x1fffff) >> 0xd) << 0x10);
        return;
      }
    }
    iVar2 = DAT_080679a0;
    uVar6 = 3;
    if (unaff_r7 != 0) {
      uVar6 = DAT_0806799c;
    }
    drawing_FUN_08022084(uVar6,(*(ushort *)(DAT_080679a0 + 2) & 0x1fff) >> 5);
    *(char *)(iVar2 + 0xb) = *(char *)(iVar2 + 0xb) + '\x01';
  } while( true );
}


