'''
41. 係り受け解析結果の読み込み（文節・係り受け）
40に加えて，文節を表すクラスChunkを実装せよ．
このクラスは
・形態素（Morphオブジェクト）のリスト（morphs），
・係り先文節インデックス番号（dst），
・係り元文節インデックス番号のリスト（srcs）
をメンバ変数に持つこととする．
さらに，入力テキストのCaboChaの解析結果を読み込み，
１文をChunkオブジェクトのリストとして表現し，
8文目の文節の文字列と係り先を表示せよ．
第5章の残りの問題では，ここで作ったプログラムを活用せよ．
'''
import sys
from no40 import Morph
import re

class Chunk(object):
    def __init__(self, chunk_lines):
        header = chunk_lines[0].split()
        self.src = int(header[1])
        self.dst = int(header[2].replace("D", ""))
        self.morphs = [Morph(line) for line in chunk_lines[1:]]
    def __repr__(self):
        bases = "".join([morph.surface for morph in self.morphs])
        return "src: {}, dst: {}, surface: {}"\
               .format(self.src, self.dst, bases)


def load_cabocha(lines):
    sents, sent, chunk_lines = [], [], []
    for line in lines:
        if line[0] == "*":
            if chunk_lines:
                sent.append(Chunk(chunk_lines))
            chunk_lines = [line]
        elif line.rstrip("\n") == "EOS":
            if chunk_lines:
                sent.append(Chunk(chunk_lines))
                sents.append(sent)
            sent = []
            chunk_lines = []
        else:
            chunk_lines.append(line)
    return sents


if __name__ == '__main__':
    f = open(sys.argv[1], 'rt')
    sents = load_cabocha(f)
    f.close()
    print(*sents[8], sep="\n")
