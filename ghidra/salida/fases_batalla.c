// ===== 080674DC FUN_080674dc

void FUN_080674dc(void)

{
  uint uVar1;
  
  uVar1 = (uint)*(byte *)(DAT_08067504 + 0xb);
  if (0xd < uVar1) {
    uVar1 = FUN_08067dac();
  }
                    /* WARNING: Could not recover jumptable at 0x08067500. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (**(code **)(uVar1 * 4 + DAT_08067508))();
  return;
}


// ===== 08067E60 FUN_08067e60

void FUN_08067e60(void)

{
  uint uVar1;
  
  uVar1 = (uint)*(byte *)(DAT_08067e88 + 0xb);
  if (0xc < uVar1) {
    uVar1 = FUN_08068c8c();
  }
                    /* WARNING: Could not recover jumptable at 0x08067e84. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (**(code **)(uVar1 * 4 + DAT_08067e8c))();
  return;
}


// ===== 08069334 FUN_08069334

undefined8 FUN_08069334(uint param_1)

{
  int iVar1;
  uint uVar2;
  bool bVar3;
  undefined4 in_lr;
  
  if ((*DAT_0806946c & 8) != 0) {
    bVar3 = true;
    if (((*(byte *)((int)DAT_0806946c + param_1 * 0x18 + 0x11) & 0x1f) == 3) &&
       (iVar1 = show_confirmation_prompt(DAT_08069470,0xff,1 << (param_1 & 0xff) & 0xffff,1,0xe,0),
       0 < iVar1)) {
      bVar3 = false;
    }
    uVar2 = *(ushort *)((int)DAT_0806946c + 2) & 0x1fff;
    if (((*(uint *)(((*(ushort *)((int)DAT_0806946c + 2) & 0x1fff) >> 5 & 0x7f) * 0x50 +
                    DAT_08069478 * (uVar2 >> 0xc) + DAT_08069474 + 0x30) & 0xfffff) >> 0xc & 0x7f)
        != 0) {
      uVar2 = (uint)*(ushort *)
                     ((*(ushort *)
                        ((uVar2 >> 5 & 0x7f) * 0x50 + DAT_08069478 * (uVar2 >> 0xc) + DAT_08069474 +
                        0x24) & 0x7fff) * 2 + DAT_0806947c);
      if ((uVar2 == DAT_08069480) || (uVar2 == DAT_08069484)) {
        bVar3 = false;
      }
      uVar2 = (uint)*(ushort *)
                     ((*(ushort *)
                        (((*DAT_0806946c & 0x1fffff) >> 0xd & 0x7f) * 0x50 +
                         DAT_08069478 * ((*DAT_0806946c & 0x1fffff) >> 0x14) + DAT_08069474 + 0x24)
                      & 0x7fff) * 2 + DAT_0806947c);
      if ((uVar2 == DAT_08069488) || (uVar2 == DAT_08069488 + 0x81)) {
        bVar3 = false;
      }
    }
    if (bVar3) {
      FUN_080314b4((1 - param_1) * -0x80000000 |
                   (*(ushort *)((int)DAT_0806946c + 2) & 0x1fff) >> 5 | 0x16600000,0);
    }
  }
  return CONCAT44(in_lr,1);
}


// ===== 0806948C FUN_0806948c

void FUN_0806948c(undefined2 *param_1)

{
  undefined2 uVar1;
  uint *puVar2;
  uint uVar3;
  undefined4 uVar4;
  int iVar5;
  int iVar6;
  uint extraout_r1;
  uint uVar7;
  uint uVar8;
  uint unaff_r4;
  code *UNRECOVERED_JUMPTABLE;
  char cStack_2c;
  char acStack_2b [3];
  uint uStack_28;
  uint uStack_24;
  
  puVar2 = puRam080694b4;
  uVar3 = (uint)*(byte *)((int)puRam080694b4 + 0xb);
  if (uVar3 == 1) {
    uVar3 = FUN_08069ddc();
  }
  if ((int)uVar3 < 2) {
    if (uVar3 != 0) {
      FUN_08069e3c();
      uVar3 = unaff_r4 >> 0x10;
      goto LAB_080694b8;
    }
  }
  else {
LAB_080694b8:
    if (uVar3 == 2) {
      FUN_08069e06();
    }
    FUN_08069e3c();
  }
  uVar3 = (uint)(byte)*puVar2;
  if (((byte)*puVar2 & 2) != 0) {
    FUN_08069e3c();
    uVar3 = extraout_r1;
  }
  iVar6 = iRam08069530;
  uVar4 = 0;
  if ((uVar3 & 1) != 0) {
    uVar3 = *puVar2;
    uVar7 = (uint)*(ushort *)
                   ((*(ushort *)
                      (((uVar3 & 0x1fffff) >> 0xd & 0x7f) * 0x50 +
                       iRam08069538 * ((uVar3 & 0x1fffff) >> 0x14) + iRam08069534 + 0x24) & 0x7fff)
                    * 2 + iRam08069530);
    if ((uVar7 != uRam0806953c) && (uVar7 != uRam08069540)) {
      FUN_08069e3c();
    }
    uVar4 = 0x3c;
    if (param_1 != (undefined2 *)0x0) {
      uVar4 = uRam08069544;
    }
    drawing_FUN_08022034(uVar4,(uVar3 & 0x1fffff) >> 0xd,0x13);
    uVar4 = FUN_08069e3c();
    uVar1 = (undefined2)iVar6;
    *(undefined2 *)(iVar6 + 0x30) = uVar1;
    *param_1 = uVar1;
  }
  cleanup_card_actions(uVar4);
  uVar4 = DAT_0806972c;
  iVar6 = DAT_080695e8;
  uVar3 = (uint)*(ushort *)((int)puVar2 + 2);
  if (((*(uint *)(((uVar3 & 0x1fff) >> 5 & 0x7f) * 0x50 + ((uVar3 & 0x1fff) >> 0xc) * DAT_080695e8 +
                  DAT_080695ec + 0x30) & 0xfffff) >> 0xc & 0x7f) == 0x11) {
    uStack_28 = 0x41;
    uVar7 = *puVar2;
    uVar8 = (uint)*(ushort *)
                   ((*(ushort *)
                      (((uVar7 & 0x1fffff) >> 0xd & 0x7f) * 0x50 +
                       ((uVar7 & 0x1fffff) >> 0x14) * DAT_080695e8 + DAT_080695ec + 0x24) & 0x7fff)
                    * 2 + DAT_080695f0);
    if (uVar8 == DAT_080695f4) {
      iVar5 = FUN_0801231c((uVar7 & 0x1fffff) >> 0xd,DAT_0806972c,1,4);
      if ((iVar5 != 0) &&
         (iVar6 = (1 - (int)param_1) * iVar6 + DAT_08069730,
         (*(byte *)(iVar6 + 0x1c) & 0x3f) != 0 || *(char *)(iVar6 + 0x1b) < '\0')) {
        FUN_08010a30(uVar4,0xff,1 << ((uint)param_1 & 0xff) & 0xffff,0x20,6,1,&cStack_2c);
        if (cStack_2c != -1) {
          FUN_0801aa84(param_1,cStack_2c);
        }
        FUN_08026adc(1 - (int)param_1,1,1);
      }
    }
    else if ((int)DAT_080695f4 < (int)uVar8) {
      if (uVar8 == DAT_08069620) {
        FUN_080234f4((int)param_1 << 0x1f | DAT_08069798 | (uVar7 & 0x1fffff) >> 0xd,
                     (uVar3 & 0x1fff) >> 5 | 0xff0000);
      }
      else {
        if ((int)DAT_08069620 < (int)uVar8) {
          uVar3 = DAT_08069638;
          if (uVar8 == DAT_08069634) goto LAB_08069674;
        }
        else {
          uVar3 = DAT_08069620 - 0xed;
        }
        if (uVar8 == uVar3) goto LAB_08069674;
      }
    }
    else if (uVar8 == DAT_080695f8) {
LAB_08069674:
      uStack_28 = 0x42;
    }
    else if ((int)DAT_080695f8 < (int)uVar8) {
      if (uVar8 == DAT_0806960c) goto LAB_08069674;
      if (((uVar8 == DAT_0806960c + 0x44) &&
          (((*(uint *)(((uVar3 & 0x1fff) >> 5 & 0x7f) * 0x50 +
                       ((uVar3 & 0x1fff) >> 0xc) * DAT_080695e8 + DAT_080696bc + 0x30) & 0xfffff) >>
            0xc & 0x7f) != 0x11)) && ((*puVar2 & 8) != 0)) {
        uStack_28 = 0;
      }
    }
    else if (uVar8 == 0x12a0) {
      FUN_0800e158((uVar7 & 0x1fffff) >> 0xd,0xe);
      return;
    }
    iVar6 = DAT_08069868;
    uVar3 = (uint)*(ushort *)(DAT_080697a4 + 2);
    uVar7 = (uint)*(ushort *)
                   ((*(ushort *)
                      (((uVar3 & 0x1fff) >> 5 & 0x7f) * 0x50 +
                       DAT_080697a8 * ((uVar3 & 0x1fff) >> 0xc) + DAT_080697a0 + 0x24) & 0x7fff) * 2
                   + DAT_0806979c);
    if (uVar7 == DAT_080697ac) {
LAB_080697bc:
      iVar5 = FUN_08015b80((*(ushort *)(DAT_08069868 + 2) & 0x1fff) >> 5);
      if (iVar5 != 0xff) {
        uVar3 = FUN_08011074(1U - (int)param_1,0);
        if (uVar3 != 0xffffffff) {
          uStack_28 = 0;
          uVar8 = (uint)*(ushort *)(iVar6 + 2);
          uVar7 = (uVar8 & 0x1fff) >> 5;
          FUN_080188ac(uVar7,(1U - (int)param_1 & 1) << 0xf | (uVar3 & 0x3f) << 4 |
                             ((*(byte *)((uVar7 & 0x7f) * 0x50 +
                                         DAT_08069870 * ((uVar8 & 0x1fff) >> 0xc) + DAT_0806986c +
                                        0x33) & 0x1f) >> 4) << 3 |
                             ((*(byte *)(((uVar8 & 0x1fff) >> 5 & 0x7f) * 0x50 +
                                         DAT_08069870 * ((uVar8 & 0x1fff) >> 0xc) + DAT_0806986c +
                                        0x33) & 0x3f) >> 5) << 2);
        }
      }
    }
    else if ((int)DAT_080697ac < (int)uVar7) {
      if ((uVar7 == DAT_080697b8) && ((*(byte *)(DAT_080697a4 + 3) & 0x40) != 0)) {
        FUN_080234f4((1 - (int)param_1) * -0x80000000 | (uVar3 & 0x1fff) >> 5 | DAT_08069970,
                     (uVar3 & 0x1fff) >> 5 | 0xff0000);
      }
    }
    else if (uVar7 == DAT_080697ac - 3) goto LAB_080697bc;
    puVar2 = DAT_08069974;
    iVar6 = FUN_0806178c((*(ushort *)((int)DAT_08069974 + 2) & 0x1fff) >> 5);
    if (iVar6 != 0xff) {
      uVar3 = FUN_08011074(1U - (int)param_1,0);
      if (uVar3 != 0xff) {
        uStack_28 = 0;
        uVar8 = (uint)*(ushort *)((int)puVar2 + 2);
        uVar7 = (uVar8 & 0x1fff) >> 5;
        FUN_080188ac(uVar7,(1U - (int)param_1 & 1) << 0xf | (uVar3 & 0x3f) << 4 |
                           ((*(byte *)((uVar7 & 0x7f) * 0x50 +
                                       DAT_0806997c * ((uVar8 & 0x1fff) >> 0xc) + DAT_08069978 +
                                      0x33) & 0x1f) >> 4) << 3 |
                           ((*(byte *)(((uVar8 & 0x1fff) >> 5 & 0x7f) * 0x50 +
                                       DAT_0806997c * ((uVar8 & 0x1fff) >> 0xc) + DAT_08069978 +
                                      0x33) & 0x3f) >> 5) << 2);
      }
    }
    if ((uStack_28 & 0x40) != 0) {
      uStack_28 = uStack_28 | ((uint)param_1 & 1) << 0xf;
      send_card_to_graveyard
                ((*(ushort *)((int)DAT_08069974 + 2) & 0x1fff) >> 5,uStack_28,
                 (*DAT_08069974 & 0x1fffff) >> 0xd);
      return;
    }
  }
  else {
    uVar3 = *puVar2;
    uVar7 = (uint)*(ushort *)
                   ((*(ushort *)
                      (((uVar3 & 0x1fffff) >> 0xd & 0x7f) * 0x50 +
                       ((uVar3 & 0x1fffff) >> 0x14) * DAT_080695e8 + DAT_08069a70 + 0x24) & 0x7fff)
                    * 2 + DAT_08069a6c);
    if ((uVar7 == DAT_08069a74) || (uVar7 == DAT_08069a78)) {
      uVar4 = 0x3c;
      if (param_1 != (undefined2 *)0x0) {
        uVar4 = DAT_08069a7c;
      }
      drawing_FUN_08022034(uVar4,(uVar3 & 0x1fffff) >> 0xd,0x13);
    }
  }
  uVar4 = DAT_08069b6c;
  iVar6 = DAT_08069a84;
  uVar3 = *DAT_08069a80;
  if (((*(uint *)(((uVar3 & 0x1fffff) >> 0xd & 0x7f) * 0x50 +
                  ((uVar3 & 0x1fffff) >> 0x14) * DAT_08069a84 + DAT_08069a70 + 0x30) & 0xfffff) >>
       0xc & 0x7f) != 0x11) goto LAB_08069dc2;
  uStack_24 = 0x41;
  uVar8 = (uint)*(ushort *)((int)DAT_08069a80 + 2);
  uVar7 = (uint)*(ushort *)
                 ((*(ushort *)
                    (((uVar8 & 0x1fff) >> 5 & 0x7f) * 0x50 +
                     ((uVar8 & 0x1fff) >> 0xc) * DAT_08069a84 + DAT_08069a70 + 0x24) & 0x7fff) * 2 +
                 DAT_08069a6c);
  if (uVar7 == DAT_08069a88) {
    iVar5 = FUN_0801231c((uVar8 & 0x1fff) >> 5,DAT_08069b6c,1,4);
    if ((iVar5 != 0) &&
       (iVar6 = (int)param_1 * iVar6 + DAT_08069b70,
       (*(byte *)(iVar6 + 0x1c) & 0x3f) != 0 || *(char *)(iVar6 + 0x1b) < '\0')) {
      FUN_08010a30(uVar4,0xff,1 << (1U - (int)param_1 & 0xff) & 0xffff,0x20,6,1,acStack_2b);
      if (acStack_2b[0] != -1) {
        FUN_0801aa84(1U - (int)param_1,acStack_2b[0]);
      }
      FUN_08026adc(param_1,1,1);
    }
  }
  else if ((int)DAT_08069a88 < (int)uVar7) {
    if (uVar7 == DAT_08069aa8) {
      FUN_080234f4((1 - (int)param_1) * -0x80000000 | DAT_08069be8 | (uVar8 & 0x1fff) >> 5,
                   (uVar3 & 0x1fffff) >> 0xd | 0xff0000);
    }
    else {
      if ((int)DAT_08069aa8 < (int)uVar7) {
        uVar3 = DAT_08069ac0;
        if (uVar7 == DAT_08069abc) goto LAB_08069afc;
      }
      else {
        uVar3 = DAT_08069aa8 - 0xed;
      }
LAB_08069ab4:
      if (uVar7 == uVar3) goto LAB_08069afc;
    }
  }
  else if (uVar7 == DAT_08069a8c) {
LAB_08069afc:
    uStack_24 = 0x42;
  }
  else {
    uVar3 = DAT_08069a94;
    if ((int)DAT_08069a8c < (int)uVar7) goto LAB_08069ab4;
    if (uVar7 == 0x12a0) {
      FUN_0800e158((uVar8 & 0x1fff) >> 5,0xe);
      return;
    }
  }
  uVar3 = *DAT_08069bf4;
  uVar7 = (uint)*(ushort *)
                 ((*(ushort *)
                    (((uVar3 & 0x1fffff) >> 0xd & 0x7f) * 0x50 +
                     DAT_08069bf8 * ((uVar3 & 0x1fffff) >> 0x14) + DAT_08069bf0 + 0x24) & 0x7fff) *
                  2 + DAT_08069bec);
  if (uVar7 == DAT_08069bfc) goto LAB_08069c8c;
  if ((int)DAT_08069bfc < (int)uVar7) {
    if ((int)uVar7 <= DAT_08069c30) {
      if (((int)uVar7 < DAT_08069c30 + -1) && (uVar7 != DAT_08069c30 - 5U)) {
        uVar3 = DAT_08069c30 - 3;
LAB_08069c28:
        if (uVar7 != uVar3) goto LAB_08069d96;
      }
      goto LAB_08069c8c;
    }
    if (uVar7 == DAT_08069c44) goto LAB_08069c8c;
    if (uVar7 == DAT_08069c48) {
      FUN_080234f4((int)param_1 << 0x1f | (uVar3 & 0x1fffff) >> 0xd | DAT_08069dd4,
                   (uVar3 & 0x1fffff) >> 0xd | 0xff0000);
    }
  }
  else {
    if (uVar7 == DAT_08069bfc - 0x50) {
LAB_08069c8c:
      iVar6 = FUN_0806178c((*DAT_08069d6c & 0x1fffff) >> 0xd);
      if ((iVar6 == 0xff) || (uVar3 = FUN_08011074(param_1,0), uVar3 == 0xff)) goto LAB_08069d96;
      uVar7 = *DAT_08069d6c;
    }
    else {
      if ((int)(DAT_08069bfc - 0x50) < (int)uVar7) {
        if (uVar7 != DAT_08069c10) {
          uVar3 = DAT_08069c10 + 0x1d;
          goto LAB_08069c28;
        }
        goto LAB_08069c8c;
      }
      if ((((uVar7 != DAT_08069c00) && (uVar7 != DAT_08069c00 + 3)) ||
          (iVar6 = FUN_08015b80((*DAT_08069c88 & 0x1fffff) >> 0xd), iVar6 == 0xff)) ||
         (uVar3 = FUN_08011074(param_1,0), uVar3 == 0xffffffff)) goto LAB_08069d96;
      uVar7 = *DAT_08069c88;
    }
    uStack_24 = 0;
    uVar7 = uVar7 & 0x1fffff;
    uVar8 = uVar7 >> 0xd;
    FUN_080188ac(uVar8,((uint)param_1 & 1) << 0xf | (uVar3 & 0x3f) << 4 |
                       ((*(byte *)((uVar7 >> 0x14) * DAT_08069d74 + (uVar8 & 0x7f) * 0x50 +
                                   DAT_08069d70 + 0x33) & 0x1f) >> 4) << 3 |
                       ((*(byte *)((uVar8 & 0x7f) * 0x50 + (uVar7 >> 0x14) * DAT_08069d74 +
                                   DAT_08069d70 + 0x33) & 0x3f) >> 5) << 2);
    uVar4 = 0x62;
    if (param_1 != (undefined2 *)0x0) {
      uVar4 = DAT_08069d78;
    }
    drawing_FUN_08022084(uVar4,(*DAT_08069d6c & 0x1fffff) >> 0xd);
    uVar4 = 0x3b;
    if (param_1 != (undefined2 *)0x0) {
      uVar4 = DAT_08069d7c;
    }
    drawing_FUN_08022034(uVar4,(*DAT_08069d6c & 0x1fffff) >> 0xd,8);
  }
LAB_08069d96:
  if ((uStack_24 & 0x40) != 0) {
    uStack_24 = uStack_24 | (1U - (int)param_1 & 1) << 0xf;
    send_card_to_graveyard
              ((*DAT_08069dd8 & 0x1fffff) >> 0xd,uStack_24,
               (*(ushort *)((int)DAT_08069dd8 + 2) & 0x1fff) >> 5);
    return;
  }
LAB_08069dc2:
  process_card_actions();
  *(char *)((int)DAT_08069dd8 + 0xb) = *(char *)((int)DAT_08069dd8 + 0xb) + '\x01';
                    /* WARNING: Could not recover jumptable at 0x08069e4c. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*UNRECOVERED_JUMPTABLE)(0);
  return;
}


// ===== 08069E50 FUN_08069e50

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_08069e50(uint param_1)

{
  ushort uVar1;
  bool bVar2;
  uint *puVar3;
  uint *puVar4;
  byte bVar5;
  short sVar6;
  uint uVar7;
  undefined4 uVar8;
  uint uVar9;
  uint *puVar10;
  int iVar11;
  byte *pbVar12;
  uint uVar13;
  int iVar14;
  int iVar15;
  code *UNRECOVERED_JUMPTABLE;
  
  cleanup_card_actions();
  puVar4 = FUN_0806a29a;
  uVar13 = uRam0806a210;
  iVar15 = iRam0806a20c;
  iVar11 = iRam0806a200;
  puVar3 = puRam08069f70;
  puVar10 = puRam08069ecc;
  uVar7 = *puRam08069ecc;
  uVar9 = (uint)*(ushort *)
                 ((*(ushort *)
                    (((uVar7 & 0x1fffff) >> 0xd & 0x7f) * 0x50 +
                     ((uVar7 & 0x1fffff) >> 0x14) * iRam08069ed0 + iRam08069ec8 + 0x24) & 0x7fff) *
                  2 + iRam08069ec4);
  if (uVar9 == uRam08069ed4) {
code_r0x08069f38:
    sVar6 = FUN_0800e158((*puRam08069f70 & 0x1fffff) >> 0xd,0xe);
    if (sVar6 != 0) {
      uVar8 = 0x3c;
      if (param_1 != 0) {
        uVar8 = uRam08069f74;
      }
      drawing_FUN_08022034(uVar8,(*puVar3 & 0x1fffff) >> 0xd,0xe);
      uVar8 = 1;
      if (param_1 != 0) {
        uVar8 = uRam08069f78;
      }
      uVar13 = *puVar3;
code_r0x0806a28c:
      drawing_FUN_08022084(uVar8,(uVar13 & 0x1fffff) >> 0xd);
    }
  }
  else if ((int)uRam08069ed4 < (int)uVar9) {
    if (iRam08069f1c < (int)uVar9) {
      if (uVar9 == uRam08069f34) {
        uVar8 = 0x3c;
        if (param_1 != 0) {
          uVar8 = _FUN_0806a358;
        }
        drawing_FUN_08022034(uVar8,(uVar7 & 0x1fffff) >> 0xd,0x1b);
        uVar8 = 1;
        if (param_1 != 0) {
          uVar8 = uRam0806a35c;
        }
        drawing_FUN_08022084(uVar8,(*puVar10 & 0x1fffff) >> 0xd);
      }
      else if (uVar9 == uRam08069f34 + 0x21) goto code_r0x0806a214;
    }
    else {
      if ((int)uVar9 < iRam08069f1c + -1) {
        if (uVar9 == iRam08069f1c - 0x82U) {
code_r0x0806a214:
          uVar7 = *FUN_0806a29a;
          uVar13 = uVar7 & 0x1fffff;
          if (((*(uint *)(((uVar7 & 0x1fffff) >> 0xd & 0x7f) * 0x50 +
                          iRam0806a2a0 * (uVar13 >> 0x14) + iRam0806a298 + 0x30) & 0xfffff) >> 0xc &
              0x7f) == 0) {
            if (*(char *)((uVar13 >> 0xd & 0x7f) * 0x50 + iRam0806a2a0 * (uVar13 >> 0x14) +
                          iRam0806a298 + 0x3a) == '\0') {
              uVar13 = (uVar7 & 0x1fffff) >> 0xd;
              send_card_to_graveyard(uVar13,(param_1 & 1) << 0xf | 0x41,uVar13);
              return;
            }
            uVar8 = 0x41;
            if (param_1 != 0) {
              uVar8 = uRam0806a2a4;
            }
            drawing_FUN_08022084(uVar8,(uVar7 & 0x1fffff) >> 0xd);
            uVar8 = 1;
            if (param_1 != 0) {
              uVar8 = uRam0806a2a8;
            }
            uVar13 = *puVar4;
            goto code_r0x0806a28c;
          }
          goto LAB_0806a2e6;
        }
        if (uVar9 != iRam08069f1c - 0x5fU) goto LAB_0806a2e6;
      }
      if ((*puRam0806a1fc & 1) != 0) goto LAB_0806a7bc;
      if (((int)((uint)*(byte *)(iRam0806a204 * param_1 + iRam0806a200 + iRam0806a208) * 0x8000000)
           < 0) && (((*(uint *)(((*(ushort *)((int)puRam0806a1fc + 2) & 0x1fff) >> 5 & 0x7f) * 0x50
                                + iRam0806a204 *
                                  ((*(ushort *)((int)puRam0806a1fc + 2) & 0x1fff) >> 0xc) +
                                iRam0806a200 + 0x30) & 0xfffff) >> 0xc & 0x7f) == 0)) {
        iVar14 = 0;
        do {
          uVar7 = FUN_0800e6a0(param_1,5,iVar14);
          if ((uVar7 != 0xff) &&
             (*(ushort *)
               ((*(ushort *)
                  ((uVar7 & 0x7f) * 0x50 + iRam0806a204 * ((int)(uVar7 & 0x80) >> 7) + iVar11 + 0x24
                  ) & 0x7fff) * 2 + iVar15) == uVar13)) {
            FUN_0801aa84(param_1,uVar7);
            break;
          }
          iVar14 = iVar14 + 1;
        } while (iVar14 < 5);
        uVar13 = (*(ushort *)((int)puRam0806a1fc + 2) & 0x1fff) >> 5;
        uVar7 = (param_1 & 1) << 0xf | 0x41;
        puVar10 = puRam0806a1fc;
LAB_0806a1ee:
        send_card_to_graveyard(uVar13,uVar7,(*puVar10 & 0x1fffff) >> 0xd);
        return;
      }
    }
  }
  else if (uVar9 == uRam08069ed8) {
    if ((puRam08069ecc[param_1 * 6 + 9] & 1) == 0) {
      uVar13 = uVar7 & 0x1fffff;
      if ((((*(uint *)(((uVar7 & 0x1fffff) >> 0xd & 0x7f) * 0x50 + (uVar13 >> 0x14) * iRam08069ed0 +
                       iRam08069ec8 + 0x30) & 0xfffff) >> 0xc & 0x7f) == 0) &&
         (-1 < (int)((uint)*(byte *)((uVar13 >> 0xd & 0x7f) * 0x50 + (uVar13 >> 0x14) * iRam08069ed0
                                     + iRam08069ec8 + 0x33) * 0x4000000))) {
        FUN_0801aaa4(param_1,(uVar7 & 0x1fffff) >> 0xd);
        FUN_0801a36c(param_1,(*puVar10 & 0x1fffff) >> 0xd,0,0);
      }
    }
  }
  else if ((int)uRam08069ed8 < (int)uVar9) {
    if (uVar9 == uRam08069ef8) {
      if ((*puRam08069ecc & 1) != 0) goto LAB_0806a7bc;
      uVar13 = (uint)*(ushort *)((int)puRam08069ecc + 2);
      bVar5 = *(byte *)(((uVar13 & 0x1fff) >> 5 & 0x7f) * 0x50 +
                        ((uVar13 & 0x1fff) >> 0xc) * iRam08069ed0 + iRam08069ec8 + 0x30) & 0x1f;
      if (((bVar5 < 4) && (1 < bVar5)) &&
         (((*(uint *)(((uVar13 & 0x1fff) >> 5 & 0x7f) * 0x50 +
                      ((uVar13 & 0x1fff) >> 0xc) * iRam08069ed0 + iRam08069ec8 + 0x30) & 0xfffff) >>
           0xc & 0x7f) == 0)) {
        FUN_0801aa84(param_1,(uVar7 & 0x1fffff) >> 0xd);
        uVar13 = (*(ushort *)((int)puVar10 + 2) & 0x1fff) >> 5;
        uVar7 = (param_1 & 1) << 0xf | 0x41;
        goto LAB_0806a1ee;
      }
    }
    else if (uVar9 == uRam08069ef8 + 1) {
      if ((*puRam08069ecc & 1) != 0) goto LAB_0806a7bc;
      uVar13 = (uint)*(ushort *)((int)puRam08069ecc + 2);
      bVar5 = *(byte *)(((uVar13 & 0x1fff) >> 5 & 0x7f) * 0x50 +
                        ((uVar13 & 0x1fff) >> 0xc) * iRam08069ed0 + iRam08069ec8 + 0x30) & 0x1f;
      if (((bVar5 == 0xf) || (bVar5 == 0x12)) &&
         (((*(uint *)(((uVar13 & 0x1fff) >> 5 & 0x7f) * 0x50 +
                      ((uVar13 & 0x1fff) >> 0xc) * iRam08069ed0 + iRam08069ec8 + 0x30) & 0xfffff) >>
           0xc & 0x7f) == 0)) {
        FUN_0801aa84(param_1,(uVar7 & 0x1fffff) >> 0xd);
        uVar13 = (*(ushort *)((int)puVar10 + 2) & 0x1fff) >> 5;
        uVar7 = (param_1 & 1) << 0xf | 0x41;
        goto LAB_0806a1ee;
      }
    }
  }
  else if ((uVar9 == uRam08069edc) || (uVar9 == uRam08069ee0)) goto code_r0x08069f38;
LAB_0806a2e6:
  uVar13 = DAT_0806a6ec;
  iVar15 = DAT_0806a6e8;
  iVar11 = DAT_0806a368;
  puVar10 = DAT_0806a360;
  if ((*DAT_0806a360 & 1) != 0) goto LAB_0806a7bc;
  uVar7 = (uint)*(ushort *)((int)DAT_0806a360 + 2);
  uVar9 = (uint)*(ushort *)
                 ((*(ushort *)
                    (((uVar7 & 0x1fff) >> 5 & 0x7f) * 0x50 +
                     ((uVar7 & 0x1fff) >> 0xc) * DAT_0806a36c + DAT_0806a368 + 0x24) & 0x7fff) * 2 +
                 DAT_0806a364);
  if (uVar9 == DAT_0806a370) {
LAB_0806a598:
    uVar13 = (uint)*(ushort *)((int)DAT_0806a360 + 2);
    uVar7 = uVar13 & 0x1fff;
    if (((*(uint *)(((uVar13 & 0x1fff) >> 5 & 0x7f) * 0x50 + DAT_0806a610 * (uVar7 >> 0xc) +
                    DAT_0806a368 + 0x30) & 0xfffff) >> 0xc & 0x7f) != 0) goto LAB_0806a7bc;
    if (*(char *)((uVar7 >> 5 & 0x7f) * 0x50 + DAT_0806a610 * (uVar7 >> 0xc) + DAT_0806a368 + 0x3a)
        == '\0') {
LAB_0806a6d8:
      uVar13 = (uVar13 & 0x1fff) >> 5;
      send_card_to_graveyard(uVar13,(1 - param_1 & 1) << 0xf | 0x41,uVar13);
      return;
    }
    uVar8 = 0x41;
    if (param_1 != 1) {
      uVar8 = DAT_0806a614;
    }
    drawing_FUN_08022084(uVar8,(uVar13 & 0x1fff) >> 5);
    uVar8 = 1;
    if (param_1 != 1) {
      uVar8 = DAT_0806a618;
    }
    uVar1 = *(ushort *)((int)puVar10 + 2);
  }
  else {
    if ((int)uVar9 <= (int)DAT_0806a370) {
      if (uVar9 == DAT_0806a374) {
        uVar13 = *DAT_0806a360 & 0x1fffff;
        bVar5 = *(byte *)(((*DAT_0806a360 & 0x1fffff) >> 0xd & 0x7f) * 0x50 +
                          (uVar13 >> 0x14) * DAT_0806a36c + DAT_0806a368 + 0x30) & 0x1f;
        if (((bVar5 < 4) && (1 < bVar5)) &&
           (((*(uint *)((uVar13 >> 0xd & 0x7f) * 0x50 + (uVar13 >> 0x14) * DAT_0806a36c +
                        DAT_0806a368 + 0x30) & 0xfffff) >> 0xc & 0x7f) == 0)) {
          FUN_0801aa84(param_1,(uVar7 & 0x1fff) >> 5);
          uVar13 = *puVar10;
          uVar1 = *(ushort *)((int)puVar10 + 2);
LAB_0806a58e:
          send_card_to_graveyard
                    ((uVar13 & 0x1fffff) >> 0xd,(1 - param_1 & 1) << 0xf | 0x41,
                     (uVar1 & 0x1fff) >> 5);
          return;
        }
      }
      else {
        if ((int)DAT_0806a374 < (int)uVar9) {
          if (uVar9 == DAT_0806a38c) {
            uVar13 = *DAT_0806a360;
            bVar5 = *(byte *)(((uVar13 & 0x1fffff) >> 0xd & 0x7f) * 0x50 +
                              ((uVar13 & 0x1fffff) >> 0x14) * DAT_0806a36c + DAT_0806a368 + 0x30) &
                    0x1f;
            if (((bVar5 == 0xf) || (bVar5 == 0x12)) &&
               (((*(uint *)(((uVar13 & 0x1fffff) >> 0xd & 0x7f) * 0x50 +
                            ((uVar13 & 0x1fffff) >> 0x14) * DAT_0806a36c + DAT_0806a368 + 0x30) &
                 0xfffff) >> 0xc & 0x7f) == 0)) {
              FUN_0801aa84(param_1,(uVar7 & 0x1fff) >> 5);
              uVar13 = *puVar10;
              uVar1 = *(ushort *)((int)puVar10 + 2);
              goto LAB_0806a58e;
            }
            goto LAB_0806a7bc;
          }
          uVar13 = DAT_0806a38c + 0xdf;
        }
        else {
          if (uVar9 == DAT_0806a378) {
            iVar11 = 1 - param_1;
            if (((DAT_0806a360[iVar11 * 6 + 9] & 1) == 0) &&
               ((int)((uint)*(byte *)(((byte)DAT_0806a360[iVar11 * 6 + 4] & 0x7f) * 0x50 +
                                      -((int)(((byte)DAT_0806a360[iVar11 * 6 + 4] & 0x80) << 0x18)
                                       >> 0x1f) * DAT_0806a36c + DAT_0806a368 + 0x33) * 0x4000000) <
                0)) {
              FUN_0801aaa4(iVar11,(uVar7 & 0x1fff) >> 5);
              FUN_0801a36c(param_1,(byte)puVar10[iVar11 * 6 + 4],0,0);
            }
            goto LAB_0806a7bc;
          }
          uVar13 = DAT_0806a378 + 0xfb;
        }
        if (uVar9 == uVar13) {
          FUN_0800e158((*(ushort *)((int)DAT_0806a360 + 2) & 0x1fff) >> 5,0xe);
          return;
        }
      }
      goto LAB_0806a7bc;
    }
    if ((int)uVar9 <= DAT_0806a3a8) {
      if (((((int)uVar9 < DAT_0806a3a8 + -1) && (uVar9 != DAT_0806a3a8 - 0x5fU)) ||
          (-1 < (int)((uint)*(byte *)(DAT_0806a6e0 * (1 - param_1) + DAT_0806a368 + DAT_0806a6e4) *
                     0x8000000))) ||
         (((*(uint *)(((*DAT_0806a360 & 0x1fffff) >> 0xd & 0x7f) * 0x50 +
                      DAT_0806a6e0 * ((*DAT_0806a360 & 0x1fffff) >> 0x14) + DAT_0806a368 + 0x30) &
           0xfffff) >> 0xc & 0x7f) != 0)) goto LAB_0806a7bc;
      iVar14 = 0;
      do {
        uVar7 = FUN_0800e6a0(param_1,5,iVar14);
        if ((uVar7 != 0xff) &&
           (*(ushort *)
             ((*(ushort *)
                ((uVar7 & 0x7f) * 0x50 + DAT_0806a6e0 * ((int)(uVar7 & 0x80) >> 7) + iVar11 + 0x24)
              & 0x7fff) * 2 + iVar15) == uVar13)) {
          FUN_0801aa84(param_1,uVar7);
          break;
        }
        iVar14 = iVar14 + 1;
      } while (iVar14 < 5);
      uVar13 = (uint)*(ushort *)(DAT_0806a6f0 + 2);
      goto LAB_0806a6d8;
    }
    if (uVar9 == DAT_0806a3c4) goto LAB_0806a598;
    if ((int)DAT_0806a3c4 < (int)uVar9) {
      if (uVar9 == DAT_0806a3d4) {
        bVar2 = true;
        iVar11 = 0;
        do {
          iVar15 = 0;
          if (bVar2) {
            pbVar12 = (byte *)(iVar11 * 0xb + DAT_0806a7d8 + DAT_0806a7d0);
            do {
              bVar5 = *pbVar12;
              if (((bVar5 != 0xff) && (uVar13 = bVar5 & 0x7f, 0x1a < uVar13 - 100)) &&
                 ((iVar14 = uVar13 * 0x50 + (uint)(bVar5 >> 7) * DAT_0806a7dc + DAT_0806a7d0,
                  (int)((uint)*(byte *)(iVar14 + 0x33) * 0x8000000) < 0 &&
                  (*(ushort *)((*(ushort *)(iVar14 + 0x24) & 0x7fff) * 2 + DAT_0806a7d4) ==
                   DAT_0806a7e0)))) {
                bVar2 = false;
              }
              pbVar12 = pbVar12 + 1;
              iVar15 = iVar15 + 1;
            } while ((iVar15 < 5) && (bVar2));
          }
        } while ((iVar11 + 1 < 2) && (iVar11 = iVar11 + 1, bVar2));
        if (bVar2) {
          uVar13 = (*(ushort *)((int)DAT_0806a360 + 2) & 0x1fff) >> 5;
          send_card_to_graveyard(uVar13,(1 - param_1 & 1) << 0xf | 0x41,uVar13);
          return;
        }
      }
      goto LAB_0806a7bc;
    }
    if (uVar9 != DAT_0806a3c4 - 0x21) goto LAB_0806a7bc;
    uVar8 = 0x3c;
    if (param_1 != 1) {
      uVar8 = DAT_0806a71c;
    }
    drawing_FUN_08022034(uVar8,(uVar7 & 0x1fff) >> 5,0x1c);
    uVar8 = 1;
    if (param_1 != 1) {
      uVar8 = DAT_0806a720;
    }
    uVar1 = *(ushort *)((int)puVar10 + 2);
  }
  drawing_FUN_08022084(uVar8,(uVar1 & 0x1fff) >> 5);
LAB_0806a7bc:
  process_card_actions();
                    /* WARNING: Could not recover jumptable at 0x0806a7ce. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*UNRECOVERED_JUMPTABLE)(1);
  return;
}


