def get_download_option():
    DOWNLOAD_OPTION = set()

    print('다운로드할 말뭉치를 하나씩 추가해주세요.')
    print()
    print('   0. 전체\n\n   1. 원시 말뭉치\n   2. 형태분석 말뭉치\n   3. 형태의미 말뭉치\n   4. 구문분석 말뭉치\n\n   9. 설정 완료')
    print()

    opt = -1
    while opt != 9 or len(DOWNLOAD_OPTION) < 1:
        opt = int(input('다운로드 옵션 추가: '))
        if opt == 9:
            if len(DOWNLOAD_OPTION) < 1:
                print('다운로드할 말뭉치를 한 개 이상 추가해야합니다.')
                continue
            else:
                print('다운로드할 말뭉치: ', end = '')
                for i in DOWNLOAD_OPTION:
                    if i == 1: print('원시 ', end = '')
                    if i == 2: print('형태분석 ', end = '')
                    if i == 3: print('형태의미 ', end = '')
                    if i == 4: print('구문분석 ', end = '')
                print()
                break
        if opt in [1, 2, 3, 4]:
            DOWNLOAD_OPTION.add(opt)
        elif opt == 0:
            DOWNLOAD_OPTION.update({1, 2, 3, 4})
            print('모든 말뭉치를 다운로드합니다.')
            break
        else:
            print('잘못 입력하셨습니다.')

    return DOWNLOAD_OPTION