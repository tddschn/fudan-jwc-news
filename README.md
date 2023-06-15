# fudan-jwc-news

Read Fudan JWC News from your terminal. 

Never check [JWC](https://jwc.fudan.edu.cn/) again!


- [fudan-jwc-news](#fudan-jwc-news)
  - [Installation](#installation)
    - [pipx](#pipx)
    - [pip](#pip)
  - [Usage](#usage)
  - [Example output](#example-output)
  - [See also](#see-also)

## Installation

### pipx

```
pipx install fudan-jwc-news
```

### pip

```
pip install fudan-jwc-news
```

## Usage

```
Usage: jwc-news [OPTIONS]

Options:
  -l, --limit INTEGER RANGE       limit the number of news  [default: 14;
                                  x<=14]
  -o, --output PATH               output file, default is stdout
  -f, --force-update              do not use cache and force update
  -v, --version                   Show the application's version and exit.
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.
```

## Example output
```
$ jwc-news -l 2
04-29 关于2022年春季学期复旦大学水平测试(补测试)考试通知
http://www.jwc.fudan.edu.cn/bf/be/c25325a442302/page.htm

04-29 2022年春季学期本科学生转专业报名名单
http://www.jwc.fudan.edu.cn/bf/bc/c25325a442300/page.htm

```

## See also

- https://github.com/tddschn/fudan-utils : Get your grades from command line, and more