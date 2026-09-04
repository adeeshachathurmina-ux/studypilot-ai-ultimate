from studypilot.documents import clean,chunks
from studypilot.models import Chunk
def test_clean_noise():assert clean('Title\n12')=='Title'
def test_chunks():assert chunks('First useful concept has enough words.\nSecond useful concept also has words.')
def test_model():assert Chunk('1','x','a.pdf',2,'M').page==2
