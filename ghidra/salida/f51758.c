// ===== 08051758 FUN_08051758

undefined8 FUN_08051758(ushort *param_1)

{
  byte bVar1;
  int iVar2;
  int iVar3;
  uint uVar4;
  int iVar5;
  int iVar6;
  uint uVar7;
  undefined4 uVar8;
  uint *puVar9;
  undefined4 in_lr;
  undefined1 auStack_a0 [128];
  
  bVar1 = (byte)*param_1;
  if ((bVar1 & 1) == 0) {
    puVar9 = (uint *)(DAT_080517f8 + 0x7c0);
    uVar4 = (*puVar9 & 0x3ffff) >> 10;
    if (uVar4 == 1) {
      fusion_summon_dialogue
                (bVar1 & 1,0x12,
                 *(undefined2 *)
                  ((*(ushort *)
                     (((*param_1 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                      DAT_08051b34 * ((*param_1 & 0x1ff) >> 8) + DAT_08051b30 + 0x24) & 0x7fff) * 2
                  + DAT_08051b2c),0);
LAB_08051b46:
      *puVar9 = DAT_08051b68 & *puVar9 | (((*puVar9 & 0x3ffff) >> 10) + 1 & 0xff) << 10;
      uVar8 = 0;
      goto LAB_08051b7c;
    }
    if (uVar4 < 2) {
      if (uVar4 == 0) {
        *(byte *)(param_1 + 4) = (byte)param_1[4] & 0xf0;
        iVar2 = DAT_080518ac;
        iVar3 = DAT_080518a8;
        iVar6 = DAT_080518a4;
        iVar5 = FUN_0805aeb0(bVar1 & 1,
                             *(undefined2 *)
                              ((*(ushort *)
                                 (((*param_1 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                                  DAT_080518ac * ((*param_1 & 0x1ff) >> 8) + DAT_080518a8 + 0x24) &
                               0x7fff) * 2 + DAT_080518a4),0);
        if (iVar5 != 0) {
          if ((*param_1 & 1) == 0) {
            uVar4 = (uint)*(ushort *)
                           ((*(ushort *)
                              (((*param_1 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                               iVar2 * ((*param_1 & 0x1ff) >> 8) + iVar3 + 0x24) & 0x7fff) * 2 +
                           iVar6);
            if (DAT_08051910 < (int)uVar4) {
              if (uVar4 == 0x1820) goto LAB_08051a58;
              if (uVar4 < 0x1821) {
                iVar6 = DAT_08051a98;
                iVar3 = DAT_08051a94;
                if (uVar4 == DAT_080519bc) {
LAB_08051aa0:
                    /* WARNING: Subroutine does not return */
                  replace_string_in_template2(auStack_a0,iVar3,iVar3 + iVar6);
                }
                if ((int)DAT_080519bc < (int)uVar4) {
                  if (uVar4 == DAT_080519d8) goto LAB_08051a58;
                  uVar7 = DAT_080519e0;
                  if ((int)uVar4 <= (int)DAT_080519d8) {
                    uVar7 = DAT_080519d8 - 0x22;
                  }
                }
                else {
                  if (uVar4 == DAT_080519bc - 0x3d) goto LAB_08051a4c;
                  uVar7 = DAT_080519c4;
                  if ((int)uVar4 <= (int)(DAT_080519bc - 0x3d)) {
                    if (uVar4 == DAT_080519bc - 0x53) {
                    /* WARNING: Subroutine does not return */
                      ask_question(DAT_08051a88);
                    }
                    goto LAB_08051ab8;
                  }
                }
              }
              else if (DAT_08051a04 < (int)uVar4) {
                if (uVar4 == DAT_08051a24) goto LAB_08051a4c;
                uVar7 = DAT_08051a30;
                if ((int)DAT_08051a24 < (int)uVar4) goto LAB_08051a2a;
                uVar7 = DAT_08051a24 - 0x4a;
              }
              else {
                if (DAT_08051a04 + -1 <= (int)uVar4) goto LAB_08051a58;
                if (uVar4 == DAT_08051a04 - 7U) {
LAB_08051a64:
                    /* WARNING: Subroutine does not return */
                  ask_question(DAT_08051a6c);
                }
                uVar7 = DAT_08051a0c;
                if ((int)uVar4 <= (int)(DAT_08051a04 - 7U)) {
                  if (uVar4 == DAT_08051a04 - 0x3cU) {
                    FUN_080e1ff0(auStack_a0,DAT_08051a7c,1);
                    /* WARNING: Subroutine does not return */
                    ask_question(auStack_a0);
                  }
                  goto LAB_08051ab8;
                }
              }
            }
            else {
              if (DAT_08051910 + -1 <= (int)uVar4) goto LAB_08051a4c;
              if (uVar4 == DAT_08051914) goto LAB_08051a58;
              if ((int)DAT_08051914 < (int)uVar4) {
                if (uVar4 == DAT_08051960) goto LAB_08051a4c;
                if ((int)uVar4 <= (int)DAT_08051960) {
                  if (uVar4 == DAT_08051960 - 0x96) goto LAB_08051a64;
                  if ((int)(DAT_08051960 - 0x96) < (int)uVar4) {
                    iVar6 = DAT_08051ab4;
                    iVar3 = DAT_08051ab0;
                    if (uVar4 == DAT_08051970) goto LAB_08051aa0;
                  }
                  else if (uVar4 == DAT_08051960 - 0x9b) goto LAB_08051a40;
                  goto LAB_08051ab8;
                }
                if (uVar4 == DAT_08051984) goto LAB_08051a58;
                uVar7 = DAT_0805198c;
                if ((int)uVar4 <= (int)DAT_08051984) {
                  uVar7 = DAT_08051984 - 0x4b;
                  goto LAB_08051a2a;
                }
              }
              else {
                if (uVar4 == DAT_08051918) {
LAB_08051a40:
                    /* WARNING: Subroutine does not return */
                  ask_question(DAT_08051a48);
                }
                if ((int)DAT_08051918 < (int)uVar4) {
                  if (uVar4 == DAT_08051930) goto LAB_08051a58;
                  uVar7 = DAT_08051938;
                  if ((int)uVar4 <= (int)DAT_08051930) {
                    uVar7 = DAT_08051930 - 0x56;
                  }
LAB_08051a2a:
                  if (uVar4 == uVar7) {
LAB_08051a58:
                    /* WARNING: Subroutine does not return */
                    ask_question(DAT_08051a60);
                  }
                  goto LAB_08051ab8;
                }
                if (uVar4 == DAT_0805191c) {
                    /* WARNING: Subroutine does not return */
                  ask_question(DAT_08051a3c);
                }
                uVar7 = DAT_0805191c + 0xd8;
              }
            }
            if (uVar4 == uVar7) {
LAB_08051a4c:
                    /* WARNING: Subroutine does not return */
              ask_question(DAT_08051a54);
            }
LAB_08051ab8:
                    /* WARNING: Subroutine does not return */
            ask_question(DAT_08051ae0);
          }
          iVar6 = FUN_08072ecc(*(ushort *)
                                (((*param_1 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                                 iVar2 * ((*param_1 & 0x1ff) >> 8) + iVar3 + 0x24) & 0x7fff,0);
          if (iVar6 != 0) {
            *puVar9 = *puVar9 & DAT_080518b0 | 0x800;
            uVar8 = 0;
            goto LAB_08051b7c;
          }
        }
        goto LAB_08051b7a;
      }
    }
    else if (uVar4 == 2) {
      drawing_FUN_08022084(2,(*(uint *)(DAT_08051b64 + 0x24) & 0x7ffff) >> 0xb);
      goto LAB_08051b46;
    }
    FUN_08051650(param_1,(*(uint *)(DAT_08051b8c + 0x24) & 0x7ffff) >> 0xb);
  }
  else {
    *(byte *)(param_1 + 4) = (byte)param_1[4] & 0xf0;
    iVar3 = FUN_08072ecc(*(ushort *)
                          (((*param_1 & 0x1ff) >> 1 & 0x7f) * 0x50 +
                           DAT_080517d0 * ((*param_1 & 0x1ff) >> 8) + DAT_080517cc + 0x24) & 0x7fff,
                         0);
    iVar6 = DAT_080517d4;
    if (iVar3 != 0) {
      drawing_FUN_08022084(2,(*(uint *)(DAT_080517d4 + 0x24) & 0x7ffff) >> 0xb);
      FUN_08051650(param_1,(*(uint *)(iVar6 + 0x24) & 0x7ffff) >> 0xb);
    }
  }
LAB_08051b7a:
  uVar8 = 1;
LAB_08051b7c:
  return CONCAT44(in_lr,uVar8);
}


