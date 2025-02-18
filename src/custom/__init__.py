from dotenv import load_dotenv
from .config import config
load_dotenv(dotenv_path=config['env'])

'''
Supported component type entrypoints

- Implement the specific entrypoint associated with your component type
- You can leave the others unimplemented

To support streaming, your implementation should be a generator: https://wiki.python.org/moin/Generators
You may also simply return the final result
'''

from .model import OpenAIModel
t2t_model = OpenAIModel(config['base_url'], config['model'],config['temperature'],config['top_p'],config['frequency_penalty'],config['presence_penalty'])

from jaison_grpc.common import STTComponentRequest, T2TComponentRequest, TTSGComponentRequest, TTSCComponentRequest
async def request_unpacker(request_iterator):
    async for request_o in request_iterator:
        match request_o:
            case STTComponentRequest():
                yield request_o.audio, request_o.sample_rate, request_o.sample_width, request_o.channels
            case T2TComponentRequest():
                yield request_o.system_input, request_o.user_input
            case TTSGComponentRequest():
                yield request_o.content
            case TTSCComponentRequest():
                yield request_o.audio, request_o.sample_rate, request_o.sample_width, request_o.channels
            case _:
                raise Exception(f"Unknown request type: {type(request_o)}")

async def start_t2t(request_iterator):
    global t2t_model
    system_input, user_input = "", ""
    async for system_input_chunk, user_input_chunk in request_unpacker(request_iterator): # receiving chunks of info through a stream
        system_input += system_input_chunk
        user_input += user_input_chunk
    for content_chunk in t2t_model(system_input,user_input):
        yield content_chunk
        
# For speech-to-text models
async def start_stt(request_iterator) -> str:
    async for audio, sample_rate, sample_width, channels in request_unpacker(request_iterator): # receiving chunks of info through a stream
        raise NotImplementedError

# For text-to-speech generation
async def start_ttsg(request_iterator) -> str:
    async for text in request_unpacker(request_iterator): # receiving chunks of info through a stream
        raise NotImplementedError

# For voice changers
async def start_ttsc(request_iterator) -> str:
    async for audio, sample_rate, sample_width, channels in request_unpacker(request_iterator): # receiving chunks of info through a stream
        raise NotImplementedError