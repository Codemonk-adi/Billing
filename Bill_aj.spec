# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['Bill_aj.py'],
             pathex=['C:\\Users\\Aaditya\\Documents\\GitHub\\Billing'],
             binaries=[],
             datas = [("Bill_aj_g.ico","."),("bill_temp_v3.pdf","."),("Wholesale_template_v4.pdf","."),("wholesale_template_igst_v2.pdf","."),("arialB.ttf","."),("Quivira.otf",".")],
            #  ("pages.py","."),("url_sender.py","."),("helpers.py","."),("data.py","."),
            #     ("database.py","."),("details.py","."),
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='Bill_aj',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          icon='Bill_aj_g.ico',
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Bill_aj')
