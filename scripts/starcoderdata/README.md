# StarCoderData 다운로드 스크립트

이 데이터셋의 모든 레코드의 `entireCode`는
[bigcode/starcoderdata](https://huggingface.co/datasets/bigcode/starcoderdata)에서 가져온 소스코드입니다.
이 스크립트는 지정한 언어의 원본 parquet 파일을 내려받아, 행마다 소스 파일 하나로 추출합니다.
추출 결과는 Sparrow SAST 분석에 쓰는 폴더 구조를 따릅니다.

| 스크립트 | 역할 | 의존성 |
|----------|------|--------|
| `download_starcoderdata.py` | 언어 존재 확인, parquet 다운로드, 소스 파일 추출, manifest 기록 | huggingface-hub, pandas, pyarrow, python-dotenv, tqdm |
| `validate_download.py` | 추출 결과 점검(파일 수, 빈 파일), 필요하면 `validation.json` 기록 | 표준 라이브러리만 사용 |

## 준비

- [uv](https://docs.astral.sh/uv/). 두 스크립트 모두 의존성을 파일 안에 선언(PEP 723)해 두었으므로
  `uv run`이 격리된 환경을 알아서 만듭니다. `pip install`이나 `pyproject.toml`은 필요 없습니다.
- gated 데이터셋인 `bigcode/starcoderdata`의 약관에 동의한 HuggingFace 계정과, 그 계정의 읽기 토큰.

토큰은 환경변수로 넘기거나, 스크립트를 실행하는 디렉터리의 `.env` 파일에 적습니다.

```text
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

저장소 루트의 `.env`와 기본 출력 디렉터리 `starcoderdata/`는 `.gitignore`에 들어 있습니다. 둘 다 커밋하지 마세요.

## 사용법

저장소 루트에서 실행합니다.

```bash
# HuggingFace에 parquet 파일이 있는 언어 목록
uv run scripts/starcoderdata/download_starcoderdata.py --list-languages

# 다운로드 없이 접근 권한과 언어 존재 여부만 확인
uv run scripts/starcoderdata/download_starcoderdata.py --language python --dry-run

# C 언어 parquet 최대 5개를 받아 소스 파일 최대 5000개 추출
uv run scripts/starcoderdata/download_starcoderdata.py --language c --max-parquet 5 --max-rows 5000

# 추출 결과를 검증하고 starcoderdata/c/validation.json 기록
uv run scripts/starcoderdata/validate_download.py --language c --max-rows 5000 --write-report
```

### 다운로드 옵션

```text
--language, -l      언어 이름 또는 별칭. 기본값: c
--max-parquet, -p   내려받을 parquet 최대 개수. 0이면 전부. 기본값: 5
--max-rows, -r      추출할 소스 파일 최대 개수. 기본값: 5000
--output-dir        출력 디렉터리. 기본값: starcoderdata
--repo-id           HuggingFace 데이터셋 저장소 id. 기본값: bigcode/starcoderdata
--src-chunk         청크 디렉터리당 소스 파일 수. 기본값: 1000
--token-env         토큰이 들어 있는 환경변수 이름. 기본값: HF_TOKEN
--dry-run           저장소 접근과 언어 존재 여부만 확인
--list-languages    현재 받을 수 있는 언어 목록 출력
```

### 검증 옵션

```text
--language, -l      언어 이름 또는 별칭 (필수)
--output-dir        출력 디렉터리. 기본값: starcoderdata
--max-rows          소스 파일 수의 상한 검사 (선택)
--allow-empty       빈 소스 파일이 있어도 실패로 보지 않음
--write-report      starcoderdata/{language}/validation.json 기록
```

## 동작 방식

- **언어 확인.** 언어 존재 여부는 HuggingFace 파일 목록으로 판단합니다. `{language}/*.parquet`가 없으면
  아무것도 쓰지 않고 실패하며, 비슷한 언어 이름을 제안합니다.
- **이어받기.** 먼저 `--max-parquet` 범위 안에서 이미 받아 둔 parquet의 행 수를 셉니다. 그것만으로
  `--max-rows`를 채울 수 있으면 더 받지 않고 기존 파일에서 추출을 이어갑니다. 모자라면 목표를 채우는 데
  필요한 다음 파일만 내려받습니다.
- **반복 실행 안전.** 이미 추출된 소스 파일은 번호로 확인해 건너뛰므로, 다시 실행하면 빠진 번호만 채웁니다.
  출력을 일관되게 유지하려면 `--language`, `--max-parquet`, `--max-rows`, `--src-chunk`를 실행마다 같게 두세요.
- **내용.** parquet의 `content` 열만 사용합니다. 첫 줄이 StarCoder 메타데이터 토큰(`<reponame>`,
  `<filename>`, `<gh_stars>` 등)이면 그 줄만 지우고, 나머지는 starcoderdata의 PII 치환 문자열까지 포함해
  그대로 기록합니다.

## 출력 구조

```text
starcoderdata/
└── {language}/
    ├── *.parquet
    ├── manifest.json            # parquet 목록, 전역 행 범위, 추출 합계
    ├── validation.json          # validate_download.py --write-report 가 기록
    └── src_code/
        ├── manifest.json        # 청크 목록과 각 청크가 나온 parquet 행 범위
        ├── 0000000/
        │   ├── 0000000.{ext}
        │   └── ...
        └── 0001000/
            └── ...
```

파일 이름은 선택한 parquet 전체에 걸친 전역 행 번호를 7자리로 0 채운 값입니다.
청크 디렉터리 하나에는 `--src-chunk`개 파일이 들어가며, 디렉터리 이름은 첫 번호입니다.

## 언어와 확장자

확장자 표는 출력 파일의 접미사만 정합니다. 표에 없는 언어는 `.txt`로 저장됩니다.

```text
c                 -> .c       java-server-pages -> .jsp     rust         -> .rs
cpp               -> .cpp     javascript        -> .js      sql          -> .sql
c-sharp           -> .cs      kotlin            -> .kt      swift        -> .swift
dart              -> .dart    php               -> .php     typescript   -> .ts
go                -> .go      python            -> .py      visual-basic -> .vb
html              -> .html    ruby              -> .rb      xslt         -> .xsl
java              -> .java
```

받는 별칭: `cs`, `csharp`, `c#`, `c++`, `js`, `jsp`, `kt`, `py`, `rb`, `rs`, `ts`, `vb`, `vbs`, `xsl`.

## 문제 해결

| 증상 | 해결 |
|------|------|
| `HF_TOKEN is not set` | `HF_TOKEN`을 export 하거나 현재 디렉터리의 `.env`에 추가합니다. |
| `Failed to list HuggingFace dataset files` | 토큰 계정이 `bigcode/starcoderdata` 약관에 동의했는지 확인하고, 저장소 id와 네트워크를 점검합니다. |
| `No parquet files found for language ...` | `--list-languages`로 출력된 이름 중 하나를 씁니다. |
| 다운로드 중단 | 같은 명령을 다시 실행합니다. 받아 둔 parquet와 추출된 소스 파일은 재사용됩니다. |
