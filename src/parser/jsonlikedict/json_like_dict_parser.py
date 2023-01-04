# Copyright (c) 2022 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
from typing import Dict

from src.model.document import Document
from src.parser.error import SPDXParsingError
from src.parser.jsonlikedict.annotation_parser import AnnotationParser
from src.parser.jsonlikedict.creation_info_parser import CreationInfoParser
from src.parser.jsonlikedict.dict_parsing_functions import raise_parsing_error_if_logger_has_messages, \
    construct_or_raise_parsing_error, parse_list_of_elements
from src.parser.jsonlikedict.extracted_licensing_info_parser import ExtractedLicensingInfoParser
from src.parser.jsonlikedict.file_parser import FileParser
from src.parser.logger import Logger
from src.parser.jsonlikedict.package_parser import PackageParser
from src.parser.jsonlikedict.relationship_parser import RelationshipParser
from src.parser.jsonlikedict.snippet_parser import SnippetParser


class JsonLikeDictParser:
    logger: Logger
    creation_info_parser: CreationInfoParser
    package_parser: PackageParser
    file_parser: FileParser
    snippet_parser: SnippetParser
    extracted_licensing_info_parser: ExtractedLicensingInfoParser
    relationship_parser: RelationshipParser
    annotation_parser: AnnotationParser

    def __init__(self):
        self.logger = Logger()
        self.creation_info_parser = CreationInfoParser()
        self.package_parser = PackageParser()
        self.file_parser = FileParser()
        self.snippet_parser = SnippetParser()
        self.extracted_licensing_info_parser = ExtractedLicensingInfoParser()
        self.relationship_parser = RelationshipParser()
        self.annotation_parser = AnnotationParser()

    def parse(self, json_like_dict: Dict) -> Document:

        fields_to_parse = [("creation_info", json_like_dict, self.creation_info_parser.parse_creation_info, False),
                           ("packages", json_like_dict.get("packages"), lambda x: parse_list_of_elements(x,
                                                                                                         self.package_parser.parse_package,
                                                                                                         self.package_parser.logger), True),
                           ("files", json_like_dict.get("files"), lambda x: parse_list_of_elements(x,
                                                                                                   self.file_parser.parse_file,
                                                                                                   self.file_parser.logger), True),
                           ("annotations", json_like_dict, self.annotation_parser.parse_all_annotations, True),
                           ("snippets", json_like_dict.get("snippets"), lambda x: parse_list_of_elements(x,
                                                                                                         self.snippet_parser.parse_snippet,
                                                                                                         self.snippet_parser.logger), True),
                           ("relationships", json_like_dict, self.relationship_parser.parse_all_relationships, True),
                           ("extracted_licensing_info", json_like_dict.get("hasExtractedLicensingInfos"),
                            lambda x: parse_list_of_elements(x,
                                                             self.extracted_licensing_info_parser.parse_extracted_licensing_info,
                                                             self.extracted_licensing_info_parser.logger), True)]

        parsed_fields = {}

        for argument_name, field, parsing_method, optional in fields_to_parse:
            if optional and not field:
                continue
            try:
                parsed_fields[argument_name] = parsing_method(field)
            except SPDXParsingError as err:
                self.logger.extend(err.get_messages())

        raise_parsing_error_if_logger_has_messages(self.logger)

        document = construct_or_raise_parsing_error(Document, parsed_fields)

        return document